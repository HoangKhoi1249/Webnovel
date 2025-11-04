import utilities as util
import os
import json
import translate as tl
import time

def collect_files(extension=".txt"):
    """Collect file paths in the novel directory.

    Args:
        extension (str, optional): File format to collect. Defaults to ".txt".

    Returns:
        tuple: Contains 2 elements:
            - With volumes: (list of volume names, 2D list containing chapter paths in each volume)
            - Without volumes: (None, list of chapter paths)

    Example:
        Directory structure with volumes:
        novels/
          my_novel/
            volume1/
              chap1.txt
              chap2.txt
            volume2/
              chap3.txt
        >>> vol_names, chapters = collect_files()
        >>> print(vol_names)
        ['volume1', 'volume2']
        >>> print(chapters)
        [['novels/my_novel/volume1/chap1.txt', 'novels/my_novel/volume1/chap2.txt'],
         ['novels/my_novel/volume2/chap3.txt']]

        Directory structure without volumes:
        novels/
          my_novel/
            chap1.txt
            chap2.txt
        >>> vol_names, chapters = collect_files() 
        >>> print(vol_names)
        None
        >>> print(chapters)
        ['novels/my_novel/chap1.txt', 'novels/my_novel/chap2.txt']
    """
    print()
    with open('config.json', 'r', encoding="UTF-8") as file:
        data_config = json.load(file)
        novel_name = data_config['novel_name']

    novel_folder = f"./novels/{novel_name}/"
    
    if util.has_subfolders(novel_folder):
        volumes_names = [d for d in os.listdir(novel_folder) if os.path.isdir(os.path.join(novel_folder, d))]
        volumes_lists = []
        # Lấy folder volume
        for volume in volumes_names:
            chapters_in_vol = []
            # Lấy từng file trong folder volume
            for chapter in os.listdir(os.path.join(novel_folder, volume)):
                chapter_path = util.normalize_path(os.path.join(novel_folder, volume, chapter))
                if chapter.endswith(extension) and not util.is_existed(chapter_path):
                    chapters_in_vol.append(
                        chapter_path
                    )
            volumes_lists.append(chapters_in_vol)
                
        return volumes_names, volumes_lists
    else:
        print("Không có tập nào ở đây! Đang bắt đầu thu thập theo chap...")
        
        chapters_path = []
        chapters_list = os.listdir(novel_folder)
        for chapter in chapters_list:
            chapter = os.path.join(novel_folder, chapter)
            if chapter.endswith(extension) and not util.is_existed(chapter):
                
                chapters_path.append (
                    util.normalize_path (
                        chapter
                                     )
                                     )
        return None, chapters_path

def save_content(origin_path, content):
    """Save content to a file in the translated directory structure.

    Args:
        origin_path (str): Original file path used to determine save location.
                          Example: './novels/story/chapter1.txt'
        content (str|list): Content to save. Can be either a string or list of strings.
                           If list, each item will be written on a new line.

    Notes:
        - Creates all necessary directories in the path if they don't exist
        - Uses analyze_save_path() to determine the save location
        - Encodes files in UTF-8 format
        - Overwrites existing files

    Example:
        >>> save_content('./novels/story/ch1.txt', 'Hello World')
        # Creates: ./translated/story/ch1.txt

        >>> save_content('./novels/story/ch1.txt', ['Line 1', 'Line 2'])
        # Creates: ./translated/story/ch1.txt with multiple lines
    """
    
    save_path = util.analyze_save_path(origin_path)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding='utf-8') as file:
        if isinstance(content, list):
            for line in content:
                file.write(line + '\n') 
        else:
            file.write(content)
    print(f"Saved to: {save_path}")
    return True

def full_translate(path):
    """Full process to collect files and save test content."""
    with open(path, 'r', encoding="UTF-8") as file:
        content = file.read()
    is_success = False
    while not is_success:
        try:
            translated_content =  tl.translate_content(content)
            save_content(path, translated_content)
            print("Dịch hoàn tất! đang bắt đầu chương tiếp theo...")
            is_success = True
            time.sleep(10)
        except Exception as e:
            print(f"Lỗi dịch: {e}. Thử lại sau 10 giây...")
            time.sleep(10)
# Test
if __name__ == "__main__":
    print("Starting file collection...")
    vol_lists, chapters_list = collect_files()
    print("Volumes found:", vol_lists)
    print(isinstance(chapters_list, list))
    save_content('./novels/test_novel/das/chapter_test.txt', 'This is a test content.')
    print(collect_files())