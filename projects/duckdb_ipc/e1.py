from e import Cli


def test_cli():
    cli = (
        Cli()
        .with_remote_ssh("i-0c1a515f52447759b.aws-ec2-manager")
        .with_workdir("/tmp")
        .with_cmd("echo 123 && sleep 3 && echo 'Hello, World1!' > test.txt")
        .with_cmd("echo 456 && sleep 4 && echo 'Hello, World2!' >> test.txt")
    )
    cli.run_con()

    result = cli.read_file("test.txt").decode()

    assert result == "Hello, World1!\nHello, World2!\n"
    cli.write_file("test.txt", "Hello, World3!\nHello, World4!\n".encode())
    result = cli.read_file("test.txt").decode()
    assert result == "Hello, World3!\nHello, World4!\n"
