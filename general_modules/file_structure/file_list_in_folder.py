import os

def list_files_in_current_folder():
    try:
        # Get the current working directory
        folder_path = os.getcwd()

        # Get a list of all items in the folder
        items = os.listdir(folder_path)

        # Filter out subfolders, keep only files
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

        # Write the list of files to a text file
        with open("file_list.txt", "size") as f:
            for file in files:
                f.write(f"{file}\n")

        return "file_list.txt"
    except Exception as e:
        return str(e)

# Example usage
list_files_in_current_folder()
