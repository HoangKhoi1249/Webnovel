import utilities as util
import chapter_process as cp
import os
import json
import translate

def main(split_volume=True):
    vol_lists, chapters_list = cp.collect_files()
    if vol_lists:
        print("Volumes found:", vol_lists)
    for chapter in chapters_list:
        if util.is_2d_list(chapters_list) and split_volume:
            for chap_path in chapter:
                print(chap_path)
        else:
            print(chapter)
main()