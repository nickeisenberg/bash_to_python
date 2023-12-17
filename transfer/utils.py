import os

def list_files_recursively(directory):
    """
    list all files within a directory and within all subdirectories
    """
    all_files = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path):
            all_files.extend(list_files_recursively(full_path))
        else:
            all_files.append(full_path)
    return all_files
