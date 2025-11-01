import utilities as util
import chapter_process as cp
import os
import json
import translate as tl

def main(split_volume=True):
    try:
        vol_lists, chapters_list = cp.collect_files()
        if vol_lists:
            print("Volumes found:", vol_lists)
        for chapter in chapters_list:
            if util.is_2d_list(chapter) and split_volume:
                if len(chapter) == 0:
                    print("Volume is empty, skipping...")
                    continue
                for chapter_path in chapter:
                    print(f"""Tìm thấy:
                        {chapter_path}""")
                    cp.full_translate(chapter_path)
                print("Đã hoàn tất một volume, bắt đầu volume tiếp theo...")
                    
                    
            else:
                print(f"""Tìm thấy:
                    {chapter}""")
                cp.full_translate(chapter)
        print("Tất cả chương đã được dịch xong!")
    except Exception as e:
        print(f"Lỗi trong quá trình dịch: {e}")
main()