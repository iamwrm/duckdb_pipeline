#!/usr/bin/env python3

import argparse
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound
from tabulate import tabulate
import sys
import time
import os
import textwrap

SSH_CONFIG_FILE = "aws-ec2-manager-ssh.config"


def list_ec2_instances(profile):
    try:
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource("ec2")

        instances = ec2.instances.all()

        table = []
        headers = [
            "Instance ID",
            "State",
            "Public IP",
            "Private IP",
            "Instance Type",
            "Availability Zone",
        ]

        for instance in instances:
            table.append(
                [
                    instance.id,
                    instance.state["Name"],
                    instance.public_ip_address if instance.public_ip_address else "N/A",
                    instance.private_ip_address,
                    instance.instance_type,
                    instance.placement["AvailabilityZone"],
                ]
            )

        if table:
            print(tabulate(table, headers, tablefmt="pretty"))
        else:
            print(
                f"No EC2 instances found in the default region for profile '{profile}'."
            )

    except ProfileNotFound:
        print(f"Error: The profile '{profile}' was not found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"An error occurred: {e}")


def start_ec2_instance(profile, instance_id):
    try:
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource("ec2")
        client = session.client("ec2")

        instance = ec2.Instance(instance_id)

        # Check instance state
        if instance.state["Name"] == "running":
            print(f"Instance {instance_id} is already running.")
            return
        elif instance.state["Name"] not in ["stopped", "stopping"]:
            print(
                f"Cannot start instance {instance_id} as it is in '{instance.state['Name']}' state."
            )
            return

        # Start the instance
        print(f"Starting instance {instance_id}...")
        response = instance.start()
        # Wait until the instance is running
        instance.wait_until_running()
        instance.reload()  # Refresh instance attributes

        # Retrieve the public IP address
        public_ip = instance.public_ip_address
        print(f"Instance {instance_id} is now running.")
        if public_ip:
            print(f"Public IP Address: {public_ip}")
        else:
            print("Public IP Address is not available.")

    except ProfileNotFound:
        print(f"Error: The profile '{profile}' was not found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def stop_ec2_instance(profile, instance_id):
    try:
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource("ec2")
        client = session.client("ec2")

        instance = ec2.Instance(instance_id)

        # Check instance state
        if instance.state["Name"] == "stopped":
            print(f"Instance {instance_id} is already stopped.")
            return
        elif instance.state["Name"] not in ["running", "pending"]:
            print(
                f"Cannot stop instance {instance_id} as it is in '{instance.state['Name']}' state."
            )
            return

        # Stop the instance
        print(f"Stopping instance {instance_id}...")
        response = instance.stop()
        # Wait until the instance is stopped
        instance.wait_until_stopped()
        instance.reload()  # Refresh instance attributes

        print(f"Instance {instance_id} has been stopped.")

    except ProfileNotFound:
        print(f"Error: The profile '{profile}' was not found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def config_ec2_instance(profile, instance_id):
    try:
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource("ec2")

        instance = ec2.Instance(instance_id)
        instance.load()  # Refresh attributes

        # Check instance state
        if instance.state["Name"] != "running":
            print(
                f"Instance {instance_id} is not running. Current state: '{instance.state['Name']}'. Please start the instance before configuring SSH."
            )
            return

        public_ip = instance.public_ip_address
        if not public_ip:
            print(f"Instance {instance_id} does not have a public IP address.")
            return

        host_alias = f"{instance_id}.aws-ec2-manager"

        ssh_config_entry = textwrap.dedent(f"""
            Host {host_alias}
                HostName {public_ip}
                User ubuntu
                StrictHostKeyChecking no
                UserKnownHostsFile=/dev/null
        """)

        # Ensure the config file exists
        if not os.path.exists(SSH_CONFIG_FILE):
            with open(SSH_CONFIG_FILE, "w") as f:
                f.write("# AWS EC2 Manager SSH Configurations\n")

        # Read existing config to check if Host entry exists
        with open(SSH_CONFIG_FILE, "r") as f:
            config_contents = f.read()

        # Remove existing Host entry if it exists
        if host_alias in config_contents:
            print(f"Host entry for {host_alias} already exists. Overwriting...")
            # Split the config into lines
            lines = config_contents.split("\n")
            new_lines = []
            skip = False
            for line in lines:
                if line.strip().startswith(f"Host {host_alias}"):
                    skip = True
                    continue
                if skip:
                    if line.startswith("Host ") and not line.startswith(
                        f"Host {host_alias}"
                    ):
                        skip = False
                    else:
                        continue
                new_lines.append(line)
            config_contents = "\n".join(new_lines)
        else:
            print(f"Adding new Host entry for {host_alias}.")

        # Append the new Host entry
        with open(SSH_CONFIG_FILE, "w") as f:
            f.write(config_contents.strip() + "\n" + ssh_config_entry.strip() + "\n")

        print(
            f"SSH configuration for instance {instance_id} added to {SSH_CONFIG_FILE}."
        )
        print(f"You can SSH into the instance using the alias '{host_alias}'.")

    except ProfileNotFound:
        print(f"Error: The profile '{profile}' was not found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="AWS EC2 Manager")
    parser.add_argument(
        "--profile", type=str, default="default", help="AWS profile name"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("ls", help="List all EC2 instances")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start a stopped EC2 instance")
    start_parser.add_argument(
        "instance_id", type=str, help="ID of the EC2 instance to start"
    )

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop a running EC2 instance")
    stop_parser.add_argument(
        "instance_id", type=str, help="ID of the EC2 instance to stop"
    )

    # Config command
    config_parser = subparsers.add_parser(
        "config", help="Generate SSH config for an EC2 instance"
    )
    config_parser.add_argument(
        "instance_id", type=str, help="ID of the EC2 instance to configure SSH for"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if not args.command:
        print("No command provided. Use -h for help.")
        sys.exit(1)

    profile = args.profile

    if args.command == "ls":
        list_ec2_instances(profile)
    elif args.command == "start":
        start_ec2_instance(profile, args.instance_id)
    elif args.command == "stop":
        stop_ec2_instance(profile, args.instance_id)
    elif args.command == "config":
        config_ec2_instance(profile, args.instance_id)
    else:
        print(f"Unknown command '{args.command}'. Use -h for help.")
        sys.exit(1)


if __name__ == "__main__":
    main()
