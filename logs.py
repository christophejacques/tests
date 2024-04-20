import os


def get_last_filename(extension: str, repertoire: str = ".") -> str:
    
    max_time: float = 0.0
    last_filename: str = ""

    for file in os.scandir(repertoire):
        if file.is_dir() or not file.name.upper().endswith(f".{extension.upper()}"):
            continue

        if file.stat().st_mtime > max_time:
            max_time = file.stat().st_mtime
            last_filename = file.name

    return last_filename


rep: str = r"c:/Users/utilisateur/AppData/Roaming/FreeFileSync/Logs"
print("Dernier fichier:", get_last_filename("html", rep))
