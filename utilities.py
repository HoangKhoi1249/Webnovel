def util.has_subfolders(fol_path):
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
    import os
    translated_path = "translated"
    os.makedirs(translated_path, exist_ok=True)
    parts = path.split('/')
    len_path = len(parts)
    if 4 >=len_path <= 5:
        del parts[0: 2]
        chapter_path = "/".join(parts)
    else:
        print("Invalid path! Error: 121")
    
    #new_path = os.path.join(".", translated_path, chapter_path)
    new_path = f"./{translated_path}/{chapter_path}"
    return new_path
    


if __name__ == "__main__":
    print(analyze_path('./novels/Advent of the Three Calamities/00004.txt'))