from pathlib import Path
import zipfile
from zipfile import ZipFile,is_zipfile
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from .manifest import Manifest
sevenzip="C:/Program Files/7-Zip/7z.exe"

def is_zipfile(filepath:Path):
    if zipfile.is_zipfile(str(filepath)):
        return True

def writeToZipfile(archive:ZipFile,pathInZipfile:Path,data:bytes|str):
    archive.writestr(Path(pathInZipfile).as_posix(),data,zipfile.ZIP_DEFLATED,9)

def createZipfile(folderToZip,newZipFilePath):
    # the new zipfile to create, minus suffix
    base_name = Path(newZipFilePath).absolute().with_suffix("")

    # the root folder of files to archive
    root_dir = folderToZip

    # the subdirectory after the root_dir, where archiving will start
    base_dir = ""

    shutil.make_archive(
        base_name,
        "zip",
        root_dir,
        base_dir,
    )
def extractWith7zip(sourceZipfile:Path,target:Path):
    command=f'"{sevenzip}" x "{sourceZipfile}" -o"{target}/"'
    subprocess.call(command)

def createZipfileWith7zip(source:Path,target:Path):
    command=f'"{sevenzip}" a "{target}" .'
    if target.exists():
        target.unlink()
    #cwd argument explained here https://stackoverflow.com/a/21406995
    subprocess.call(command,cwd=source)

class Archive:
    def __init__(self,path:Path) -> None:
        self.path=path

    def read(self):
        return bytes()

    def namelist(self):
        """Return a list of file names in the archive."""
        output= subprocess.check_output([sevenzip, "l", "-slt", self.path.as_posix()]).decode().splitlines()
        file_paths = [  ]
        for line in output:
            if line.startswith("Path ="):
                file_paths.append(line[7:])
        if len(file_paths)>1:
            return file_paths[1:]
        else:
            return []
