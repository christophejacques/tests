import pathlib

FILEPATH = pathlib.Path(__file__).parent 

# print(FILEPATH.exists())
help(pathlib.Path.glob)
for file in pathlib.Path(__file__).parent.glob("*"):
    print("d" if file.is_dir() else "r" if file.is_file() else "-", file.parent, end="/")
    print(file.stem)
    print(file.home())
    break
