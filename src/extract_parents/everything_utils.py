from pathlib import Path
import csv

everything_path = "C:/Program Files/Everything/Everything.exe"

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


def write_paths_to_efu(paths: list[Path], outfile: Path):
    headers = ["Filename", "Size", "Date Modified", "Date Created", "Attributes"]
    with open(outfile, "w", encoding="utf8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for path in paths:
            try:
                writer.writerow({
                    "Filename": str(path),
                    "Size": path.stat().st_size,
                    "Date Modified": int(path.stat().st_mtime),
                    "Date Created": int(path.stat().st_ctime),
                    "Attributes": path.stat().st_file_attributes
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
