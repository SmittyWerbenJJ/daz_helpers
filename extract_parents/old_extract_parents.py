import os
from pathlib import Path
import tkinter as tk

from threading import Thread
import csv


def make_efu(paths: list[Path]):
    """
    efu(csv file) = Filename,Size,Date Modified,Date Created,Attributes

    """
    header = "Filename,Size,Date Modified,Date Created,Attributes"
    efuLines = [header]
    for path in paths:
        filename = "\"" + str(path.absolute()) + "\""
        size = path.stat().st_size
        date_modified = path.stat().st_mtime_ns
        date_created = path.stat().st_ctime_ns
        attributes = path.stat().st_file_attributes

        line = f"{filename},{size},{date_modified},{date_created},{attributes}"
        efuLines.append(line)

    return "\n".join(efuLines)


def path_to_str(path: Path):
    return str(path) + ""


def parse_input_file(infile) -> list[Path]:
    paths = []
    with open(infile, "r") as fp:
        for line in fp:
            paths.append(Path(line.strip()))
    return paths


def on_button_press(event):
    pass


def extract_parent_paths_to_efu(paths: list[Path], outfile: Path):
    headers = ["Filename", "Size", "Date Modified", "Date Created", "Attributes"]
    with open(outfile, "w", encoding="utf8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for path in paths:
            try:
                parent = path.parent
                writer.writerow({
                    "Filename": parent,
                    "Size": parent.stat().st_size,
                    "Date Modified": parent.stat().st_mtime,
                    "Date Created": parent.stat().st_ctime,
                    "Attributes": None
                })
            except BaseException:
                pass


def extract_parent_paths_to_txt(paths: list[Path], outfile: Path, showGUI=False):
    with open(outfile, "w") as fp:
        if paths is None:
            return
        for path in paths:
            fp.write(str(path) + "\n")
    if not showGUI:
        return


def main():
    infile = Path(__file__).parent.joinpath("extractparents_in.txt")
    outfile = Path(__file__).parent.joinpath("extractparents_out.txt")
    efuFile = Path(__file__).parent.joinpath("extractparents_out.efu")

    parsedinput = parse_input_file(infile)
    extract_parent_paths_to_txt(parsedinput, outfile)
    extract_parent_paths_to_efu(parsedinput, efuFile)


if __name__ == "__main__":
    main()


# outtext=[f"\"{str(l)}\"|" for l in lines]
# outtext[-1]=outtext[-1].replace("|","")
# outfile.write_text("\n".join(outtext))

# efu_list = make_efu(outlines)
# unique_paths = list(set(map(str, outlines)))
# efuFile.write_text(efu_list)
