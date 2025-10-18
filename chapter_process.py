import utilities as util
import os
import json

def collect_files(extension=".txt"):
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
            
            print(volume)
            chapters_in_vol = []
            # Lấy từng file trong folder volume
            for chapter in os.listdir(os.path.join(novel_folder, volume)):
                
                if chapter.endswith(extension):
                    chapters_in_vol.append(os.path.join(novel_folder, volume, chapter))
            volumes_lists.append(chapters_in_vol)
            print(chapters_in_vol)
                
        return volumes_names, volumes_lists
    else:
        print("Không có tập nào ở đây! Đang bắt đầu thu thập theo chap...")
        
        chapters_path = []
        for chapter in os.listdir(novel_folder):
            if chapter.endswith(extension):
                print(f"Tìm thấy {chapter}")
                
                chapters_path.append(os.path.join(novel_folder, chapter))
        return None, chapters_path

def save_content(origin_path, content):
    save_path = util.analyze_path(origin_path)
    for line in content:
        with open(save_path, 'w', encoding='utf-8') as file:
            if isinstance(content, list):
                for line in content:
                    file.write(line + '\n') 
            else:
                file.write(content)
        pass

# Test
if __name__ == "__main__":
    print("Starting file collection...")
    vol_lists, chapters_list = collect_files()
    print("Volumes found:", vol_lists)
    print(isinstance(chapters_list, list))
