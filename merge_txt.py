import argparse
import os
from pathlib import Path


def merge_files(input_dir, output_file, sort_numerically=True, add_separator=False, separator="\n---\n", sep_name_pattern=None):
    """
    Merge all .txt files from a directory into a single output file.
    
    Args:
        input_dir: Directory containing .txt files to merge
        output_file: Output file path
        sort_numerically: If True, sort files numerically (00001, 00002, ...)
        add_separator: If True, add separator between files
        separator: Separator string to insert between files
        sep_name_pattern: Optional pattern for separator with file name (e.g., "\\n\\n[{name_file}]\\n\\n")
    
    Returns:
        Number of files merged
    """
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise ValueError(f"Input directory not found: {input_dir}")
    
    # Get all .txt files
    txt_files = list(input_path.glob("*.txt"))
    
    if not txt_files:
        raise ValueError(f"No .txt files found in {input_dir}")
    
    # Sort files
    if sort_numerically:
        # Try numeric sort (for files like 00001.txt, 00002.txt)
        try:
            txt_files.sort(key=lambda x: int(x.stem))
        except ValueError:
            # Fall back to alphabetical sort if numeric sort fails
            txt_files.sort()
    else:
        txt_files.sort()
    
    # Merge files
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("w", encoding="utf-8") as fout:
        for idx, file in enumerate(txt_files):
            # Add newline before writing (except for the first file)
            if idx > 0:
                fout.write("\n")
            
            with file.open("r", encoding="utf-8") as fin:
                content = fin.read()
                fout.write(content)
            
            # Add separator between files (not after the last one)
            if idx < len(txt_files) - 1:
                if sep_name_pattern:
                    # Use separator pattern with file name
                    sep_text = sep_name_pattern.format(name_file=file.stem)
                    fout.write(sep_text)
                elif add_separator:
                    # Use standard separator
                    fout.write(separator)
    
    return len(txt_files)


def batch_merge(input_dir, output_dir, sort_numerically=True, add_separator=False, separator="\n---\n", sep_name_pattern=None):
    """
    Batch merge: for each subdirectory in input_dir, merge its .txt files into a single output file.
    
    Returns:
        (total_dirs_processed, total_files_merged, failed_dirs)
    """
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise ValueError(f"Input directory not found: {input_dir}")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    total_dirs = 0
    total_files = 0
    failed = 0
    
    # Process each subdirectory
    for subdir in sorted(input_path.iterdir()):
        if not subdir.is_dir():
            continue
        
        txt_files = list(subdir.glob("*.txt"))
        if not txt_files:
            continue
        
        try:
            out_file = output_path / f"{subdir.name}.txt"
            count = merge_files(
                subdir,
                out_file,
                sort_numerically=sort_numerically,
                add_separator=add_separator,
                separator=separator,
                sep_name_pattern=sep_name_pattern
            )
            print(f"  {subdir.name}: merged {count} file(s) -> {out_file.name}")
            total_dirs += 1
            total_files += count
        except Exception as e:
            print(f"  {subdir.name}: FAILED - {e}")
            failed += 1
    
    return total_dirs, total_files, failed


def main():
    parser = argparse.ArgumentParser(description="Merge all .txt files from a folder into a single file.")
    parser.add_argument("input", nargs="?", help="Input directory containing .txt files (omit with --batch)")
    parser.add_argument("-o", "--output", help="Output file path (or output directory for --batch)")
    parser.add_argument("--no-sort", action="store_true", help="Disable numeric sorting (use alphabetical)")
    parser.add_argument("--sep", action="store_true", help="Add separator between files")
    parser.add_argument("--sep-text", default="\n---\n", help="Custom separator text (default: '\\n---\\n')")
    parser.add_argument("--sep-npath", help="Custom separator with file name pattern (e.g., '\\n\\n[{name_file}]\\n\\n')")
    parser.add_argument("--batch", action="store_true", help="Batch mode: merge each subdirectory separately")
    
    args = parser.parse_args()
    
    try:
        if args.batch:
            if not args.input:
                parser.print_help()
                return 1
            if not args.output:
                args.output = f"{args.input}_merged"
            
            total_dirs, total_files, failed = batch_merge(
                args.input,
                args.output,
                sort_numerically=not args.no_sort,
                add_separator=args.sep,
                separator=args.sep_text,
                sep_name_pattern=args.sep_npath
            )
            print(f"Batch complete: {total_dirs} dir(s), {total_files} file(s) merged, {failed} failed.")
            return 0
        else:
            if not args.input or not args.output:
                parser.print_help()
                return 1
            
            count = merge_files(
                args.input,
                args.output,
                sort_numerically=not args.no_sort,
                add_separator=args.sep,
                separator=args.sep_text,
                sep_name_pattern=args.sep_npath
            )
            print(f"Merged {count} file(s) into: {args.output}")
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
"""
# Basic merge (numeric sort by default)
python merge_txt.py novels_txt/folder -o output.txt

# Merge with separators between files
python merge_txt.py novels_txt/folder -o output.txt --sep

# Alphabetical sort (no numeric)
python merge_txt.py novels_txt/folder -o output.txt --no-sort

# Custom separator
python merge_txt.py novels_txt/folder -o output.txt --sep --sep-text "\n\n===CHAPTER BREAK===\n\n"

# Custom separator with file name
python merge_txt.py novels_txt/folder -o output.txt --sep-npath "\n\n[{name_file}]\n\n"

# Batch mode with file name separator
python merge_txt.py novels_txt_split -o novels_merged --batch --sep-npath "\n\n[{name_file}]\n\n"
"""