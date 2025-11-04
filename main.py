import utilities as util
import chapter_process as cp


def main(split_volume=True):
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

    try:
        vol_lists, chapters_list = cp.collect_files()
        if vol_lists:
            print("Volumes found:", vol_lists)
        if util.is_2d_list(chapters_list) and split_volume:
            for vol in chapters_list:
                for chap in vol:
                    cp.full_translate(chap)
        else:
            for chap in chapters_list:
                cp.full_translate(chap)
        print("Tất cả chương đã được dịch xong!")
    except Exception as e:
        print(f"Lỗi trong quá trình dịch: {e}")
main()