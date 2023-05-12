"""Rough script for updating a fork when you have to manually download the source repository."""

import zipfile
import os
import shutil
import subprocess

def main():
    # Input 1: zip file
    zip_file = 'your_zip_file.zip'
    
    # Input 2: existing git project directory
    git_project_dir = 'your_git_project_directory'
    
    # Change current directory to the git project directory
    os.chdir(git_project_dir)
    
    # Step 1: Delete all files in the directory besides .git
    for file_or_dir in os.listdir():
        if file_or_dir != '.git':
            file_or_dir_path = os.path.join(git_project_dir, file_or_dir)
            if os.path.isfile(file_or_dir_path):
                os.remove(file_or_dir_path)
            elif os.path.isdir(file_or_dir_path):
                shutil.rmtree(file_or_dir_path)
    
    # Step 2: Unzip Input 1 into the directory
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(git_project_dir)
    
    # Step 3: Commit all changes using git
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Push updates from source'])
    
    # Step 4: Push all changes
    subprocess.run(['git', 'push'])

if __name__ == '__main__':
    main()
