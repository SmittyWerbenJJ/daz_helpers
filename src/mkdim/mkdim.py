"""
This script is adapted from https://gist.github.com/esemwy/7d2bfe581691418b1b82
"""
import uuid
import os
from zipfile import ZipFile, is_zipfile
import argparse
from pathlib import Path
import shutil
import zipfile

from . import progressReport,ziputils
from .mkdim_archive import Archive
from .archivedata import Archivedata
from .mkdim_types import SourceType

# To avoid confusing with DAZ3D product codes, some special ranges need to be used, so the following ranges has been reserved:
#
# - 3xxxxxxx    for Hivewire3D                         , where xxxxxxx is the product number without the prefix letter.
# - 4xxxxxxx    for RuntimeDNA                         , where xxxxxxx is the product number without the prefix letter.
# - 5xxxxxxx    for Most Digital Creations products    , where xxxxxxx is the product number without the prefix letter.
# - 6xxxxxxx    for Sharecg products                   , where xxxxxxx is the reference number.
# - 7xxxxxxx    for Renderosity products               , where xxxxxxx is RO number.
# - 8xxxxxxx    for Wilmap's Digital Creations products, where xxxxxxx is SKU number.
# - 9xxxxxxx    is reserved for your own products      , and can be numbered as your convenience.
#
# ie: the SKU 41367 (Renderotica SFD pubic hair for V5) will be converted in an zip archive named IM80041367-00_SFDPubicHairForV5.zip
#
# Another tips is to add the "CVN" letters at the end of the productname, so that it can be easily identified as "converted".

dsx = """\
<?xml version="1.0" encoding="UTF-8"?>
<ProductSupplement VERSION="0.1">
 <ProductName VALUE="{pname}"/>
 <ProductStoreIDX VALUE="{pidx}-{psubidx}"/>
 <UserOrderId VALUE="{orderid}"/>
 <UserOrderDate VALUE="{orderdate}"/>
 <InstallerDate VALUE="{installerdate}"/>
 <ProductFileGuid VALUE="{guid}"/>
 <InstallTypes VALUE="Content"/>
 <ProductTags VALUE="DAZStudio4_5"/>
</ProductSupplement>
"""
dsa="""\
// DAZ Studio version 4.10.0.123 filetype DAZ Script

if( App.version >= 67109158 ) //4.0.0.294
{
	var oFile = new DzFile( getScriptFileName() );
	var oAssetMgr = App.getAssetMgr();
	if( oAssetMgr )
	{
		oAssetMgr.queueDBMetaFile( oFile.baseName() );
	}
}
"""

manifest_header = """\
<DAZInstallManifest VERSION="0.1">
 <GlobalID VALUE="{}"/>"""
manifest_line = """ <File TARGET="Content" ACTION="Install" VALUE="{}"/>"""
manifest_footer = """</DAZInstallManifest>
"""

supplement = """\
<ProductSupplement VERSION="0.1">
 <ProductName VALUE="{}"/>
 <InstallTypes VALUE="Content"/>
 <ProductTags VALUE="DAZStudio4_5"/>
</ProductSupplement>
"""
class AssetPath:
    def __init__(self,filepath) -> None:
        strpath=str(filepath)
        i=strpath.casefold().rfind("content"+ os.sep)

        self.zippath=Path(strpath[i:])
        self.contentPath=Path(str(self.zippath)[8:])
# -------------------------------
# string fixxing
# -------------------------------

def addContentToNewArchive(sourcePath:Path,newArchive:ZipFile,relativeSourcePath:Path=Path("")):
    manifest = [manifest_header.format(str(uuid.uuid4()))]
    if is_zipfile(sourcePath):
        archive=ZipFile(sourcePath,"r")
        for file in[Path(x) for x in archive.namelist() if not Path(x).is_dir()]:
            assetpath=AssetPath(file)
            manifest.append(manifest_line.format(str(assetpath.contentPath).replace("&", "&amp;")))
            data=archive.read(file)
            ziputils.writeToZipfile(newArchive,assetpath.zippath.as_posix(),data)
    else:
        for file in [x for x in sourcePath.rglob("*") if not x.is_dir()]:
            assetpath=AssetPath(file)
            manifest.append(manifest_line.format(str(assetpath.contentPath).replace("&", "&amp;")))
            data=file.read_bytes()
            ziputils.writeToZipfile(newArchive,assetpath.zippath.as_posix(),data)
    manifest.append(manifest_footer)
    return manifest

def addDirContent(source: Path, archive: ZipFile):
    manifest = [manifest_header.format(str(uuid.uuid4()))]
    for file in source.rglob("*"):
        amp_file = Path(str(file).replace("&", "&amp;"))
        relativeContentPath = Path("Content/").joinpath(file.relative_to(source))
        amp_relativeContentPath = Path("Content/").joinpath(amp_file.relative_to(source))
        manifest.append(manifest_line.format(str(amp_relativeContentPath)))
        archive.write(file, relativeContentPath,zipfile.ZIP_DEFLATED)
    manifest.append(manifest_footer)
    return manifest


def addZipContent(source: Path, newArchive: ZipFile):
    with ZipFile(source, "r") as archive:
        manifest = [manifest_header.format(str(uuid.uuid4()))]
        filelist = [item for item in archive.namelist() if not item.endswith("/")]

        for item in filelist:
            filePath = Path("Content").joinpath(item.replace("&", "&amp;"))
            manifest.append(manifest_line.format(filePath))
            ziputils.writeToZipfile(newArchive,str(filePath), archive.read(item))
        addPromoImageFromFilelist(source,filelist,newArchive)
    manifest.append(manifest_footer)
    return manifest

def addPromoImageFromFilelist(source,filelist,newArchive):
    """Finds and adds Images as Promo Images

    Args:
        source (_type_): _description_
        filelist (_type_): _description_
        newArchive (_type_): _description_
    """
def readSourceContent(source:Path,contentPath:Path)->bytes:
    """Read content from a source

    Args:
        source (Path): The Source Folder or Archive
        contentPath (Path): The Path relative from the source

    Returns:
        bytes: the Data
    """
    if is_zipfile(source):
        return ZipFile(source).read(contentPath.as_posix())

    return source.joinpath(contentPath).read_bytes()




def createManifestFromFileList(filelist: list[Path]):
    manifest = [manifest_header.format(str(uuid.uuid4()))]
    filelist = [item for item in filelist if not item.is_dir()]

    for file in filelist:
        str_file = str(file).replace("&", "&amp;")
        filePath = Path("Content").joinpath(str_file)
        manifest.append(manifest_line.format(str(filePath)))
    manifest.append(manifest_footer)
    return manifest


def createManifest(source: Path, archive: ZipFile):
    """create manifest from source. this will put the files from the source-tree in the archive

    Args:
        source (Path): source folder or archive
        archive (ZipFile): destination archive for files to be placed inside

    """

    if is_zipfile(source):
        manifest = createManifestFromFileList([Path(x) for x in ZipFile(source,"r").namelist])
        manifest = addZipContent(source, archive)
    else:
        manifest = createManifestFromFileList([x.relative_to(source) for x in source.rglob("*")])
        manifest = addDirContent(source, archive)
    return manifest


def createManifest_reparent(
    source: Path, archive: ZipFile, filelist: list[Path], newRoot: Path
):
    """create manifest from source. this will put the files from the source-tree in the archive
    Additionally we will reparent the files from `filelist` to `newRoot` so that:
        some/path/to/Content/data -> Content/data

    """
    relativeFilelist=[file.relative_to(newRoot) for file in filelist]
    manifest = createManifestFromFileList(relativeFilelist)
    for file in filelist:
        fullpath = source.joinpath(file)
        if fullpath.suffix=="":
            continue

        content=readSourceContent(source,file)
        arcPath  = Path(str(file).replace(str(newRoot),"Content/"))

        ziputils.writeToZipfile(archive,arcPath.as_posix(),content)

    return manifest


def pack(filepath: str, destinationFolder="", callback_report=None):
    def nullCallback(**args):
        return

    if callback_report is None:
        callback_report = nullCallback

    _archive = Archive(Path(filepath).absolute())

    if _archive.source.sourceType is SourceType.INVALID:
        message = f"""\
        Source is not organized correctly. Make Sure the Root paths are the same as in your Daz Library or are Compatible with DIM")
        Source: {filepath}
        """
        callback_report(
            progressReport.ProgressReport(message).setMessageType(
                progressReport.MessageType.INFO
            )
        )
        return
    try:
        _archive.processArchive(destinationFolder, callback_report)
    except PermissionError as e:
        callback_report(
            progressReport.ProgressReport(f"Permission Error while Processing {filepath}!\nMaybe the archives are opened somewhere?").setMessageType(
                progressReport.MessageType.ERROR
            )
        )
    except Exception as e:
        callback_report(
            progressReport.ProgressReport(f"Error while Processing {filepath}!\n{e}").setMessageType(
                progressReport.MessageType.ERROR
            )
        )




def main_from_cli():
    parser = argparse.ArgumentParser(description="Make DAZ Install manager ZIP and metadata.")
    parser.add_argument(
        "sources",
        metavar="directory or zip",
        type=list[str],
        help="Source Folders or Zip-Archives",
        nargs="+",
    )

    args = parser.parse_args()

    for arg in args.sources:
        pack(arg)


import threading


class mkdimThread(threading.Thread):
    def __init__(self, filepaths: list[str], destinationFolder: str, callback_report) -> None:
        super(mkdimThread, self).__init__()

        self.filepaths = filepaths
        self.destinationFolder = destinationFolder
        self.callback_report = callback_report

    def run(self):
        for filepath in self.filepaths:
            pack(filepath, self.destinationFolder, self.callback_report)
            self.callback_report(
                progressReport.ProgressReport(Path(filepath).name).setMessageType(
                    progressReport.MessageType.FINISHED_ONE
                )
            )
        self.callback_report(
            progressReport.ProgressReport().setMessageType(
                progressReport.MessageType.FINISHED_COMPLETELY
            )
        )


if __name__ == "__main__":
    main_from_cli()
