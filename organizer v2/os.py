import os
import shutil
import json
from inquirer import prompt
from inquirer.questions import List
import re
from colorama import init, Fore


download_dir = "C:/Users/dell/Downloads"
destination_dir = "E:/Study"
# Load the folder mapping from the JSON file

with open("E:/map.json", "r") as f:
    folder_map = json.load(f)

init(autoreset=True)

files_to_move = {}

def create_directories(destination_dir, folder_map, indentation=""):

    for folder_name, folder_info in folder_map.items():
        folder_path = os.path.join(destination_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        #     print(f"{Fore.LIGHTCYAN_EX}{indentation}{folder_name}*{Fore.RESET}")
        # else:
        #     print(f"{Fore.WHITE}{indentation}{folder_name}{Fore.RESET}")

        subfolders = folder_info.get('subfolders', {})
        if subfolders:
            create_directories(folder_path, subfolders, indentation=indentation + "    ")


def get_files_to_move(download_dir, destination_dir, folder_map):
    for root, _, files in os.walk(download_dir):
        for file in files:
            file_path = os.path.join(root, file)
            for folder_name, folder_info in folder_map.items():
                keywords = folder_info.get('keywords', [])
                extensions = folder_info.get('extensions', [])
                for keyword in keywords:
                    pattern = r'\b{}\b'.format(re.escape(keyword))
                    if re.search(pattern, file, re.IGNORECASE):
                        destination_path = os.path.join(destination_dir, folder_name)
                        files_to_move[file_path] = destination_path
                        break
                    # else:
                    #     print(f"No matching keyword found for file: {file}")


def display_files_to_move():

    for file_path, destination in files_to_move.items():
        print(f"{file_path.replace(download_dir, "")}{Fore.MAGENTA} \n\t>> {Fore.RESET}{Fore.YELLOW}{destination}{Fore.RESET}\n")


def get_user_confirmation():
    print("\n")
    choices = ['Yes', 'No']
    questions = [List('choice', message="Move all items?", choices=choices)]
    answer = prompt(questions)
    choice = answer['choice']
    return choice == 'Yes'


def move_files():
    for file_path, destination in files_to_move.items():
        shutil.move(file_path, destination)

def main():

    # print("\n\nThe current folder structure\n")

    create_directories(destination_dir, folder_map)

    print("\n\nThe files that are going to be moved\n")

    get_files_to_move(download_dir,destination_dir, folder_map)

    display_files_to_move()

    if get_user_confirmation():
        move_files()
        print("Files moved successfully!")
    else:
        print("Operation aborted.")

main()