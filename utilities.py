def has_subfolders(fol_path):
    """Check if a directory contains any subdirectories.

    Args:
        fol_path (str): Path to the directory to check.

    Returns:
        bool: True if directory contains subdirectories, False otherwise.

    Example:
        >>> has_subfolders("./novels/my_novel")
        True  # If my_novel contains volume folders
        >>> has_subfolders("./novels/my_novel/volume1")
        False  # If volume1 only contains files
    """
    from os import scandir
    for entry in scandir(fol_path):
        if entry.is_dir():
            return True
    return False

def is_2d_list(lst):
    """Check if a list contains nested lists (2D list).

    Args:
        lst (list): The list to check.

    Returns:
        bool: True if list contains nested lists, False otherwise.

    Example:
        >>> is_2d_list([[1, 2], [3, 4]])
        True
        >>> is_2d_list([1, 2, 3])
        False
    """
    if not isinstance(lst, list):
        return False
    return any(isinstance(item, list) for item in lst)

def analyze_save_path(path):
    """Process file path and create translated file structure.

    Args:
        path (str): Original file path using forward slashes.

    Returns:
        str: New path in the translated folder structure.

    Example:
        >>> analyze_path('./novels/my_novel/chapter1.txt')
        './translated/my_novel/chapter1.txt'

    Notes:
        - Creates 'translated' directory if it doesn't exist
        - Expects path depth of 4-5 levels
        - Removes first two path components ('./' and 'novels/')
    """
    import os

    translated_path = "translated"
    os.makedirs(translated_path, exist_ok=True)
    parts = path.split('/')
    len_path = len(parts)

    if 3 <=len_path <= 5:
        del parts[0: 2]
        chapter_path = "/".join(parts)
    else:
        print("Invalid path! Error 121")
        return None
    
    #new_path = os.path.join(".", translated_path, chapter_path)
    new_path = f"./{translated_path}/{chapter_path}"
    return new_path



def normalize_path(path):
    import re
    # Thay thế tất cả các chuỗi gồm \ hoặc / lặp lại bằng một dấu /
    return re.sub(r"[\\/]+", "/", path)

def has_existed(path):
    pass
    


if __name__ == "__main__":
    print(analyze_save_path('./novels/Advent of the Three Calamities/da/00004.txt'))
