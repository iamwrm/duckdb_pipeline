import sys
from pydantic_settings import BaseSettings, CliApp, SettingsError


# class Settings(BaseSettings, cli_parse_args=True, cli_exit_on_error=False):
class Settings(BaseSettings):
    this_foo: str

    def cli_cmd(self) -> None:
        print("Start Cli")
        # Print the parsed data
        # print(self.model_dump())
        # > {'this_foo': 'is such a foo'}

        # Update the parsed data showing cli_cmd ran
        self.this_foo = "ran the foo cli cmd"


if __name__ == "__main__":
    try:
        # sys.argv = ["example.py", "--bad-arg"]
        sys.argv = ["example.py", "--this_foo", "is such a foo"]
        # sys.argv = ["--this_foo", "is such a foo"]
        s = CliApp.run(Settings, cli_args=sys.argv)
    except SettingsError as e:
        pass
        # print(e)
