from pydantic import BaseModel
from typing import Dict, List
import subprocess
import os
import asyncio
from loguru import logger
import sys
import fcntl

# Configure loguru loggers
logger.remove()
logger.add(lambda msg: print(f"\033[32m{msg}\033[0m", flush=True), filter=lambda record: "stdout" in record["extra"])
logger.add(lambda msg: print(f"\033[31m{msg}\033[0m", flush=True, file=sys.stderr), filter=lambda record: "stderr" in record["extra"])

class Cli(BaseModel):
    workdir: str = "/tmp/"
    env: Dict[str, str] = {}
    commands: List[str] = []

    def with_workdir(self, workdir: str) -> 'Cli':
        self.workdir = workdir
        return self

    def with_env(self, env: Dict[str, str]) -> 'Cli':
        self.env.update(env)  
        return self

    def with_cmd(self, cmd: str) -> 'Cli':
        self.commands.append(cmd)
        return self

    def _set_non_blocking(self, pipe):
        fd = pipe.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def _process_output(self, proc: subprocess.Popen) -> None:
        self._set_non_blocking(proc.stdout)
        self._set_non_blocking(proc.stderr)
        
        while proc.poll() is None:
            try:
                stdout_line = proc.stdout.readline() if proc.stdout else None
                if stdout_line:
                    logger.bind(stdout=True).info(stdout_line.decode().strip())
            except (IOError, BlockingIOError):
                pass

            try:
                stderr_line = proc.stderr.readline() if proc.stderr else None
                if stderr_line:
                    logger.bind(stderr=True).error(stderr_line.decode().strip())
            except (IOError, BlockingIOError):
                pass

        # Read any remaining output
        for line in proc.stdout:
            logger.bind(stdout=True).info(line.decode().strip())
        for line in proc.stderr:
            logger.bind(stderr=True).error(line.decode().strip())

    def run_seq(self) -> None:
        merged_env = {**os.environ.copy(), **self.env}
        
        for cmd in self.commands:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                cwd=self.workdir,
                env=merged_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=False
            )
            self._process_output(proc)
            
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd)

    async def _run_cmd_async(self, cmd: str) -> None:
        merged_env = {**os.environ.copy(), **self.env}
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            cwd=self.workdir,
            env=merged_env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        async def read_stream(stream, is_stdout=True):
            while True:
                line = await stream.readline()
                if not line:
                    break
                if is_stdout:
                    logger.bind(stdout=True).info(line.decode().strip())
                else:
                    logger.bind(stderr=True).error(line.decode().strip())

        await asyncio.gather(
            read_stream(proc.stdout, True),
            read_stream(proc.stderr, False)
        )

        await proc.wait()
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd)

    def run_con(self) -> None:
        async def main():
            tasks = [self._run_cmd_async(cmd) for cmd in self.commands]
            await asyncio.gather(*tasks)

        asyncio.run(main())