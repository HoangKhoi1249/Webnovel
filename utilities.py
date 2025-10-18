def has_subfolders(fol_path):
    from os import scandir
    for entry in scandir(fol_path):
        if entry.is_dir():
            return True
    return False

def is_2d_list(lst):
    if not isinstance(lst, list):
        return False
    return any(isinstance(item, list) for item in lst)

def analyze_path(path):
    path = path.split('/')
    return path


if __name__ == "__main__":
    print(analyze_path('./novels/Advent of the Three Calamities/00004.txt'))