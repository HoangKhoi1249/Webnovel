import utilities as util
import chapter_process as cp
import os
import json
import translate

def main():
    vol_lists, chapters_list = cp.collect_files()
    if vol_lists:
        print("Volumes found:", vol_lists)
    print(chapters_list[0])
main()