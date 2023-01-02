import argparse
import os
from pathlib import Path
from typing import Union, Final

from colorama import Fore


def has_triggers(dir: Path, triggers: list[str]) -> bool:
    for trigger in triggers:
        if not (dir / Path(trigger)).exists():
            return False

    return True


def run_command_in_dir(path: Union[Path, str], command: str, trigger: list[str], ignore_folder: list[str]):
    ignore_folder = ignore_folder if ignore_folder else []
    for dir in path.iterdir():
        if dir.is_dir():
            if dir.name not in ignore_folder:
                if has_triggers(dir, trigger):
                    os.chdir(dir)
                    print(f"{Fore.GREEN}{dir}{Fore.RESET}")
                    os.system(command)
                else:
                    run_command_in_dir(dir, command, trigger, ignore_folder)
            else:
                run_command_in_dir(dir, command, trigger, ignore_folder)


def main():
    program_description = """
    Program description:
    script who iterates in directories and run command, can have trigger (specific directory or file), 
    in this case command will execute if directory contains trigger \n
    
    example : 
        
        python cmidir.py --path "../some path/" --command "some command"  --trigger ".git" --trigger "file.txt" 
        
        python g:\scripts\python\cmidir.py --command "git pull" --path "g:\cool" --ignore-folder "linux" --ignore-folder "tabulate" --trigger ".git"
    """

    parser = argparse.ArgumentParser(
        prog="Iterate and execute with triggers",formatter_class=argparse.RawDescriptionHelpFormatter, description=program_description)
    parser.add_argument("--path", type=str, dest="path", help="input path where script will run",
                        required=True)
    parser.add_argument("--command", type=str, dest="command",
                        help="input the command to be executed", required=True)
    parser.add_argument("--trigger", type=str, dest="trigger", action="append",
                        help="input trigger file or dir name, in this case command will run if trigger exists in path ")
    parser.add_argument("--ignore-folder", type=str,
                        dest="ignore_folder", action="append")

    cmd_arguments = parser.parse_args()

    dir_path: Final[Path] = Path(cmd_arguments.path)
    command: Final[str] = cmd_arguments.command
    trigger: Final[list[str]] = cmd_arguments.trigger
    ignore_folders: Final[list[str]] = cmd_arguments.ignore_folder

    if dir_path.exists():
        print(f"{Fore.GREEN}SUCCESS: {Fore.RESET}exists path \"{dir_path.absolute()}\"")
        if ignore_folders:
            print(f"{Fore.BLUE}Ignored folders :\n"+"\n".join(ignore_folders))
        run_command_in_dir(dir_path, command, trigger, ignore_folders)
        os.chdir(dir_path)

    else:
        print(
            f"{Fore.RED}ERROR: {Fore.RESET}doesn't exists path \"{dir_path.absolute()}\"")


if __name__ == '__main__':
    main()
