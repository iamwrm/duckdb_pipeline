from e import Cli

if __name__ == "__main__":
    cli = Cli()
    cli.with_cmd("echo 123 && sleep 3 && echo 'Hello, World1!'")
    cli.with_cmd("echo 456 && sleep 3 && echo 'Hello, World2!'")
    cli.run_con()
