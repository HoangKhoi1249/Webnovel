
import os
import atexit
import traceback
import re
from datetime import datetime

class TranslateLogger:

    def __init__(self):
        self.StartTime = datetime.now()
        self.SuccessCount = 0
        self.FailCount = 0
        self.BlockCount = 0
        self.RetryCount = 0

        self.BlockedFiles = []
        self.FailedFiles = []

        os.makedirs("logs", exist_ok=True)

        FileName = self.StartTime.strftime("%Y-%m-%d_%H-%M-%S") + ".log"
        self.LogPath = os.path.join("logs", FileName)

        with open(self.LogPath, "w", encoding="utf-8") as Log:
            Log.write("=== TRANSLATE SESSION START ===\n")
            Log.write(f"Start Time: {self.StartTime}\n\n")

        # Tự động ghi summary khi chương trình kết thúc
        atexit.register(self.finalize)

    # =============================
    # Ghi log cơ bản
    # =============================
    def write(self, Message, Level="INFO"):
        TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        LogLine = f"[{TimeStamp}] [{Level}] {Message}\n"

        try:
            with open(self.LogPath, "a", encoding="utf-8") as Log:
                Log.write(LogLine)
        except:
            pass

    # =============================
    # Các trạng thái
    # =============================
    def success(self, FilePath=None):
        self.SuccessCount += 1
        if FilePath:
            self.write(f"SUCCESS: {FilePath}", "SUCCESS")

    def fail(self, FilePath=None, Error=None):
        self.FailCount += 1
        if FilePath:
            self.FailedFiles.append(FilePath)
            self.write(f"FAIL: {FilePath}", "ERROR")
        if Error:
            self.write(str(Error), "ERROR")

    def block(self, FilePath=None):
        self.BlockCount += 1
        if FilePath:
            self.BlockedFiles.append(FilePath)
            self.write(f"BLOCKED: {FilePath}", "BLOCK")

    def retry(self, FilePath=None):
        self.RetryCount += 1
        if FilePath:
            self.write(f"RETRY: {FilePath}", "RETRY")

    def quota_exceeded(self, FilePath=None):
        self.QuotaCount += 1
        if FilePath:
            self.write(f"QUOTA EXCEEDED: {FilePath}", "QUOTA")

    # =============================
    # Ghi lỗi exception đầy đủ
    # =============================
    def log_exception(self, Error):
        Trace = traceback.format_exc()
        self.write(str(Error), "EXCEPTION")
        self.write(Trace, "TRACE")

    # =============================
    # Tổng kết cuối phiên
    # =============================
    def finalize(self):
        EndTime = datetime.now()
        Duration = EndTime - self.StartTime

        Summary = "\n=== SESSION SUMMARY ===\n"
        Summary += f"End Time      : {EndTime}\n"
        Summary += f"Duration      : {Duration}\n"
        Summary += f"Success       : {self.SuccessCount}\n"
        Summary += f"Failed        : {self.FailCount}\n"
        Summary += f"Blocked       : {self.BlockCount}\n"
        Summary += f"Quota Exceeded: {self.QuotaCount}\n"
        Summary += f"Retried       : {self.RetryCount}\n\n"
        Summary += f"Total Processed: {self.SuccessCount + self.FailCount + self.BlockCount + self.QuotaCount}\n\n"

        if self.BlockedFiles:
            Summary += "---- BLOCKED FILES ----\n"
            for File in self.BlockedFiles:
                Summary += f"{File}\n"
            Summary += "\n"

        if self.FailedFiles:
            Summary += "---- FAILED FILES ----\n"
            for File in self.FailedFiles:
                Summary += f"{File}\n"
            Summary += "\n"

        try:
            with open(self.LogPath, "a", encoding="utf-8") as Log:
                Log.write(Summary)
        except:
            pass

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

    # Replace backslashes and multiple slashes with a single forward slash
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
    if translated_path is None:
        return False
    return os.path.exists(translated_path)
    
    


if __name__ == "__main__":
    print(analyze_save_path('./novels/Advent of the Three Calamities/da/00004.txt'))
