import subprocess
import os
import asyncio
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Cli:
    workdir: str = "/tmp/"
    env: Dict[str, str] = field(default_factory=dict)
    commands: List[str] = field(default_factory=list)

    def with_workdir(self, workdir: str) -> 'Cli':
        self.workdir = workdir
        return self

    def with_env(self, env: Dict[str, str]) -> 'Cli':
        self.env.update(env)
        return self

    def with_cmd(self, cmd: str) -> 'Cli':
        self.commands.append(cmd)
        return self

    def _process_output(self, proc: subprocess.Popen) -> None:
        while True:
            output = proc.stdout.readline()
            if output == b'' and proc.poll() is not None:
                break
            if output:
                print(output.decode().strip())

    def run_seq(self) -> None:
        """Run commands sequentially"""
        merged_env = {**os.environ.copy(), **self.env}
        
        for cmd in self.commands:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                cwd=self.workdir,
                env=merged_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=0,
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
            stderr=asyncio.subprocess.STDOUT
        )

        while True:
            line = await proc.stdout.readline()
            if not line:
                break
            print(line.decode().strip())

        await proc.wait()
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd)

    def run_con(self) -> None:
        """Run commands concurrently"""
        async def main():
            tasks = [self._run_cmd_async(cmd) for cmd in self.commands]
            await asyncio.gather(*tasks)

        asyncio.run(main())

if __name__ == "__main__":
    cli = Cli()
    cli.with_cmd("echo 123 && sleep 3 && echo 'Hello, World1!'")
    cli.with_cmd("echo 456 && sleep 3 && echo 'Hello, World2!'")
    cli.run_con()
