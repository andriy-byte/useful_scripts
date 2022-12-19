import argparse
import os
from pathlib import Path
from typing import Union, Final

from colorama import Fore


def triggers_exists(dir: Path, triggers: list[str]) -> bool:
    for trigger in triggers:
        if not (dir / Path(trigger)).exists():
            return False

    return True


def run_command_in_dir(path: Union[Path, str], command: str, trigger: list[str]):
    for dir in path.iterdir():
        if dir.is_dir():
            if triggers_exists(dir, trigger):
                os.chdir(dir)
                print(dir)
                os.system(command)
            else:
                run_command_in_dir(dir, command, trigger)


def main():
    program_description = "script who iterates in directories and run command, can have trigger (specific directory or file)," \
                          " in this case command will execute if directory contains trigger \n" \
                          "example : python cmidir.py --path \"../some path/\" --command \"some command\" --trigger \".git\" --trigger \"file.txt\" "

    parser = argparse.ArgumentParser(prog="Iterate and execute with triggers", description=program_description)
    parser.add_argument("--path", type=str, dest="path", help="input path where script will run",
                        required=True)
    parser.add_argument("--command", type=str, dest="command",
                        help="input the command to be executed", required=True)
    parser.add_argument("--trigger", type=str, dest="trigger", action="append",
                        help="input trigger file or dir name, in this case command will run if trigger exists in path ")

    cmd_arguments = parser.parse_args()

    dir_path: Final[Path] = Path(cmd_arguments.path)
    command: Final[str] = cmd_arguments.command
    trigger: Final[list[str]] = cmd_arguments.trigger

    if dir_path.exists():
        print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}exists path \"{dir_path.absolute()}\"")
        run_command_in_dir(dir_path, command, trigger)
        os.chdir(dir_path)

    else:
        print(f"{Fore.RED}ERROR: {Fore.RESET}doesn't exists path \"{dir_path.absolute()}\"")


if __name__ == '__main__':
    main()
