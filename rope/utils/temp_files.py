import os

def cleanup_temp_files(temp_files:list[str]):
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except OSError as e:
            print(f"Error: {temp_file} : {e.strerror}")

def make_temp_file(input_line:list[str], file_name:str) -> str:
    temp_file = "temp_" + file_name + ".txt"
    with open(temp_file, "w") as f:
        f.write(f"> {file_name}\n")
        for line in input_line:
            f.write(line)
    return temp_file

def make_temp_files(input_lists:list[list[str]], file_names:list[str]) -> list[str]:
    temp_files = []
    for index, input_line in enumerate(input_lists):
        temp_file = make_temp_file(input_line, file_names[index])
        temp_files.append(temp_file)
    return temp_files