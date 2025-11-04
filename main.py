import utilities as util
import chapter_process as cp
import os
import translate as tl

def main(split_volume=True):
    try:
        vol_lists, chapters_list = cp.collect_files()
        if vol_lists:
            print("Volumes found:", vol_lists)
        if util.is_2d_list(chapters_list) and split_volume:
            for vol in chapters_list:
                for chap in vol:
                    tl.translate_chapter(chap)
        else:
            for chap in chapters_list:
                cp.full_translate(chap)
        print("Tất cả chương đã được dịch xong!")
    except Exception as e:
        print(f"Lỗi trong quá trình dịch: {e}")
main()