
import os
import re
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

    for entry in os.scandir(fol_path):
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


    translated_path = "translated"
    os.makedirs(translated_path, exist_ok=True)
    parts = path.split('/')
    len_path = len(parts)

    if 3 <=len_path <= 5:
        del parts[0: 2]
        chapter_path = "/".join(parts)
    else:
        print(f"Invalid path! Error 121 | Path depth: {len_path} | Path: {path}")
        
        return None
    
    #new_path = os.path.join(".", translated_path, chapter_path)
    new_path = f"./{translated_path}/{chapter_path}"
    return new_path



def normalize_path(path):
    """Normalize file path separators.

    Args:
        path (str): File path with mixed separators.

    Returns:
        str: Path with all separators normalized to forward slashes (/).

    Examples:
        >>> normalize_path('path\\to\\file')
        'path/to/file'
        >>> normalize_path('path/to\\file')
        'path/to/file'
    """

    # Thay thế tất cả các chuỗi gồm \ hoặc / lặp lại bằng một dấu /
    return re.sub(r"[\\/]+", "/", path)

def is_existed(path):
    """Check if translated version of a file exists.

    Args:
        path (str): Original file path.

    Returns:
        bool: True if translated file exists, False otherwise.

    Examples:
        >>> is_existed('./novels/story/chapter1.txt')
        True  # If ./translated/story/chapter1.txt exists
        >>> is_existed('./novels/story/new_chapter.txt')
        False  # If translated file doesn't exist
    """

    translated_path = analyze_save_path(path)
    if os.path.exists(translated_path):
        return True
    else:
        return False
    
    


if __name__ == "__main__":
    print(analyze_save_path('./novels/Advent of the Three Calamities/da/00004.txt'))
