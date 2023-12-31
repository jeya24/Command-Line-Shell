import os
import shutil
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer

command_history = []


def print_error(message):
    print(f"\033[91mError: {message}\033[0m")


def print_success(message):
    print(f"\033[92m{message}\033[0m")


def create_file(filename):
    try:
        with open(filename, "w") as file:
            print_success(f"Created file: {filename}")
    except IOError as e:
        print_error(f"Error creating file: {e}")


def create_folder(dirname):
    try:
        os.mkdir(dirname)
        print_success(f"Created directory: {dirname}")
    except FileExistsError:
        print(f"Directory already exists: {dirname}")
    except OSError as e:
        print_error(f"Error creating directory: {e}")


def list_files(directory="."):
    try:
        files = os.listdir(directory)
        for file in files:
            print(file)
    except FileNotFoundError:
        print_error(f"Directory not found: {directory}")
    except PermissionError as e:
        print_error(f"Permission error: {e}")


def delete_file(filename):
    try:
        os.remove(filename)
        print_success(f"Deleted file: {filename}")
    except FileNotFoundError:
        print_error(f"File not found: {filename}")
    except PermissionError as e:
        print_error(f"Permission error: {e}")
    except IsADirectoryError:
        print_error(
            f"'{filename}' is a directory. Use 'rmfolder' to delete directories."
        )


def delete_folder(dirname):
    try:
        os.rmdir(dirname)
        print_success(f"Deleted directory: {dirname}")
    except FileNotFoundError:
        print_error(f"Directory not found: {dirname}")
    except PermissionError as e:
        print_error(f"Permission error: {e}")
    except OSError as e:
        print_error(f"Error deleting directory: {e}")


def change_directory(directory):
    try:
        os.chdir(directory)
        print_success(f"Changed directory to: {directory}")
    except FileNotFoundError:
        print_error(f"Directory not found: {directory}")
    except PermissionError as e:
        print_error(f"Permission error: {e}")


def current_directory():
    print_success(f"Current directory: {os.getcwd()}")


def help_command():
    print("Available commands:")
    print("file <filename> - Create a file")
    print("folder <dirname> - Create a folder")
    print(
        "all [<directory>] - List files and folders in the specified directory (default is current directory)"
    )
    print("rmfile <filename> - Delete a file")
    print("rmfolder <dirname> - Delete a folder")
    print("goto <directory> - Change the current directory")
    print("cfolder - Display the current directory")
    print("history - Display command history")
    print("exit - Exit the program")
    print("help - Display this help message")
    print("rename <old_filename> <new_filename> - Rename a file")
    print("copy <source> <destination> - Copy a file")
    print("move <source> <destination> - Move a file")


def parse_and_execute_command(command):
    tokens = command.split()
    if not tokens:
        return

    cmd = tokens[0]

    command_history.append(command)

    if cmd == "file" and len(tokens) == 2:
        create_file(tokens[1])
    elif cmd == "folder" and len(tokens) == 2:
        create_folder(tokens[1])
    elif cmd == "all" and len(tokens) <= 2:
        list_files(tokens[1] if len(tokens) == 2 else ".")
    elif cmd == "rmfile" and len(tokens) == 2:
        delete_file(tokens[1])
    elif cmd == "rmfolder" and len(tokens) == 2:
        delete_folder(tokens[1])
    elif cmd == "goto" and len(tokens) == 2:
        change_directory(tokens[1])
    elif cmd == "cfolder":
        current_directory()
    elif cmd == "exit":
        return False
    elif cmd == "history":
        for idx, hist_cmd in enumerate(command_history):
            print(f"{idx + 1}: {hist_cmd}")
    elif cmd == "help":
        help_command()
    elif cmd == "rename" and len(tokens) == 3:
        rename_file(tokens[1], tokens[2])
    elif cmd == "copy" and len(tokens) == 3:
        copy_file(tokens[1], tokens[2])
    elif cmd == "move" and len(tokens) == 3:
        move_file(tokens[1], tokens[2])
    else:
        print_error("Invalid command. Type 'help' for a list of available commands.")

    return True


def rename_file(old_filename, new_filename):
    try:
        os.rename(old_filename, new_filename)
        print_success(f"Renamed file: {old_filename} to {new_filename}")
    except FileNotFoundError:
        print_error(f"File not found: {old_filename}")
    except PermissionError as e:
        print_error(f"Permission error: {e}")


def copy_file(source, destination):
    try:
        shutil.copy2(source, destination)
        print_success(f"Copied file from {source} to {destination}")
    except FileNotFoundError:
        print_error(f"File not found: {source}")
    except PermissionError as e:
        print_error(f"Permission error: {e}")


def move_file(source, destination):
    try:
        shutil.move(source, destination)
        print_success(f"Moved file from {source} to {destination}")
    except FileNotFoundError:
        print_error(f"File not found: {source}")
    except PermissionError as e:
        print_error(f"Permission error: {e}")


def main():
    style = PromptStyle.from_dict(
        {
            "prompt": "#800080",
            "pygments.input": "#884444",
            "pygments.commands": "#884444 bold",
        }
    )

    completer = WordCompleter(
        [
            "file",
            "folder",
            "all",
            "rmfile",
            "rmfolder",
            "goto",
            "cfolder",
            "exit",
            "history",
            "help",
            "rename",
            "copy",
            "move",
        ]
    )

    lexer = PygmentsLexer(BashLexer)
    while True:
        command = prompt(
            "Enter a command: ",
            lexer=lexer,
            style=style,
            history=FileHistory("history.txt"),
            completer=completer,
        )

        if not parse_and_execute_command(command):
            break


if __name__ == "__main__":
    main()
