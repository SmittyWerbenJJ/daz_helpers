from pathlib import Path
import zipfile
from zipfile import ZipFile,is_zipfile
import shutil

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
