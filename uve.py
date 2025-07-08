import subprocess
import sys
import argparse

def generate_uv_commands(parsed_args) -> list[str]:
    if parsed_args.command == "env" and parsed_args.subcommand == "list":
        # /b Displays a bare list of directories and files, with no additional information
        # /a attributes --> d: directories
        return ["dir /b /a:d %UVE_DIR%\\envs"]

    env_name = parsed_args.env_name

    if parsed_args.command == "create":
        packages = parsed_args.packages
        for package in packages:
            if package.startswith('python='):
                _, _, python_version = package.partition('=')
                packages.remove(package)
                break

        uv_commands = [
            f"uv venv %UVE_DIR%\\envs\\{env_name} --python {python_version}"
        ]
        if parsed_args.packages:
            uv_commands.append(
                f"uv pip install --python %UVE_DIR%\\envs\\{env_name} " + " ".join(parsed_args.packages)
            )

    else:
        cmd = parsed_args.command
        uv_commands = [
            f"uv pip {cmd} --python %UVE_DIR%\\envs\\{env_name} " + " ".join(parsed_args.packages)
        ]

    return uv_commands

def ask_yes_no(question: str) -> bool:
    while True:
        response = input(f"{question} (yes/no): ")
        if response.lower() in ["yes", "y"]:
            return True
        elif response.lower() in ["no", "n"]:
            return False
        else:
            print("Invalid response")

def execute_command(command: str):
    try:
        result=subprocess.run(
            command, check=True, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'Error executing {command}: {e}')
        exit(1)

def main():
    # print(f"Debug info: {__file__}")
    # print(f"Executable: {sys.executable}")
    # print('-' * 80)
    parser = argparse.ArgumentParser(description='Convert conda commands to uv commands.')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for create
    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('-n', '--env-name', required=True, help='Environment name')
    create_parser.add_argument('packages', nargs='*', help='Packages to install')

    # Subparser for install
    install_parser = subparsers.add_parser('install')
    install_parser.add_argument('-n', '--env-name', required=True, help='Environment name')
    install_parser.add_argument('packages', nargs='+', help='Packages to install')

    # Subparser for uninstall
    uninstall_parser = subparsers.add_parser('uninstall')
    uninstall_parser.add_argument('-n', '--env-name', required=True, help='Environment name')
    uninstall_parser.add_argument('packages', nargs='+', help='Packages to uninstall')

    # Subparser for env list
    env_parser = subparsers.add_parser('env')
    env_parser.add_argument('subcommand', choices=['list'], help='Subcommand for env')

    args = parser.parse_args(sys.argv[1:])

    if args.command is None:
        print("No command line arguments provided.")
        exit(1)

    print("UV Commands generated:")
    uv_commands = generate_uv_commands(args)
    for command in uv_commands:
        print(f' -- {command}')

    if ask_yes_no("Execute these commands"):
        for command in uv_commands:
            execute_command(command)
    else:
        print("Commands not executed")

if __name__ == "__main__":
    main()
