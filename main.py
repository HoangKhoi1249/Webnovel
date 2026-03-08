from sqlite3 import Time
import time
import utilities as util
import chapter_process as cp
import sys
import utilities as util
from colorama import Fore, Style # type: ignore
from datetime import datetime


def main(split_volume=True, log = None):
    """Process and translate novel chapters from a source directory.

    This function handles both volume-based and flat directory structures.
    It collects files, processes them chapter by chapter, and handles translation
    with error recovery.

    Args:
        split_volume (bool, optional): Whether to process chapters by volume structure.
            If True, maintains volume folder structure.
            If False, processes all chapters sequentially.
            Defaults to True.

    Returns:
        None

    Examples:
        >>> main()  # Process with volume structure
        >>> main(split_volume=False)  # Process as flat structure

    Notes:
        - Requires config.json with API settings
        - Expects novels in './novels/{novel_name}/' directory
        - Creates translated files in './translated/' directory
        - Handles translation errors with retry mechanism

    """

    logger = log if log else util.TranslateLogger()

    Time = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"

    print(Fore.BLUE + f"{Time} Phiên bản: {sys.version}")
    max_retries = 1

    with open('key.txt', 'r', encoding='utf-8') as f:
        keys = [line.strip() for line in f]

    with open('model.txt', 'r', encoding='utf-8') as m:
        models = [line.strip() for line in m]

    try:
        vol_lists, chapters_list = cp.collect_files()
        
        
        if vol_lists:
            print(Fore.GREEN + f"{Time} Volumes found: {vol_lists}")

        if util.is_2d_list(chapters_list) and split_volume:
            all_chapters = [chap for vol in chapters_list for chap in vol]
        else:
            all_chapters = chapters_list

        for chap in all_chapters:
            print(Fore.BLUE + f"{Time} Đang dịch: {chap}...")

            key_index = 0
            success = False

            while key_index < len(keys) and not success:

                API_KEY = keys[key_index]
                print(
                    Fore.BLUE + f"{Time} Thử dịch với key: {key_index} - {API_KEY}"
                      )
                model_success = False
                model_index = 0

                while model_index < len(models) and not model_success:
                    MODEL = models[model_index]
                    retry = 0

                    while retry < max_retries:

                        try:
                            print(Fore.BLUE + f"{Time} Còn {len(keys)} key và {len(models)} model \n(lần {retry + 1}/{max_retries})")
                            cp.full_translate(
                                chap,
                                API_KEY,
                                MODEL
                            )
                            
                            
                            logger.success(chap)
                            model_success = True
                            success = True
                            time.sleep(10)  # Optional: Add delay between retries
                            break  # Exit retry loop on success
                        except Exception as e:
                            retry += 1
                            logger.fail(chap, e)
                            logger.retry(chap)
                            
                            error_message = str(e)
                            if "quota" in error_message.lower():
                                model_died = Fore.RED + f"{Time} Chạm limit của model!"
                                logger.model_died(model=MODEL)
                                print(model_died)
                                if retry >= max_retries:
                                    model_index += 1
                                    logger.fail(chap, "Quota exceeded, switching model.")
                                    if model_index < len(models):    
                                        print(Fore.YELLOW + f"{Time} Đổi sang model tiếp theo: {models[model_index]}")
                                    else:
                                        print(Fore.YELLOW + f"{Time} Hết model, sẽ thử lại với key tiếp theo.")
                                logger.quota_exceeded(chap)
                            elif "PROHIBITED_CONTENT" or "block" in error_message:
                                print(Fore.RED + f"{Time} Chương bị cấm hoặc bị chặn!")

                                logger.block(chap)
                                model_success = True
                                success = True  # Mark as successful to move to next chapter
                            


                if not model_success:
                    key_dead_msg = Fore.RED + f"{Time} Key chết → xóa: {API_KEY}"
                    logger.key_died(key=API_KEY, msg=key_dead_msg)
                    print(key_dead_msg)
                    keys.pop(key_index)
                    time.sleep(2)  # Optional: Add delay after removing a key

                else:
                    break

            if not success:
                raise Exception(f"{Time} Hết toàn bộ key!")
            
        print(Fore.GREEN + f"{Time} Tất cả chương đã được dịch xong!")

    except Exception as e:
        print(Fore.RED + f"{Time} Lỗi trong quá trình dịch: {e}")

log = util.TranslateLogger()
while True:
    main(log=log)
    print(Fore.YELLOW + f"{Time} Đang khởi động lại quá trình dịch sau 5 phút...")
    time.sleep(300)  # Optional: Add delay before restarting the process