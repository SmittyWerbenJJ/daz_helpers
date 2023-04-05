import os
import zipfile
from zipfile import ZipFile

from pathlib import Path
import hashlib
import re
from . import mkdim_types
from .myTimer import MyTimer

def findProductID(path: Path):
    """find a product id from the path or the folder's name.
    alternatively generates a random product ID
    update:
    find product id in support dsx file
    """
    strpath = str(path)
    id = None
    is_zipfile = zipfile.is_zipfile(strpath)
    match = re.search(r"\d{5,}", strpath)

    if match:
        id = int(match.group(0))
    elif is_zipfile:
        archive = ZipFile(strpath)
        for file in archive.namelist():
            if "runtime/support/" in file.casefold() and file.casefold().endswith(".dsx"):
                dsxText = archive.read(file).decode("utf8")
                match = re.search(r'(ProductToken VALUE\=")(\d.*)(")', dsxText)
                id = int(match.group(2))

    elif not is_zipfile:
        # foldersearch
        filelist = path.rglob("*")
        for file in filelist:
            if (
                "runtime/support/" in file.absolute().__str__().casefold()
                and file.suffix == ".dsx"
            ):
                dsxText = file.read_text("utf8")
                match = re.search(r'(ProductToken VALUE\=")(\d.*)(")', dsxText)
                id = int(match.group(2))
    if id is None:
        # return hashed ID
        filename = path.stem
        sha1 = hashlib.sha1(filename.encode())
        hashed = int(sha1.hexdigest(), 16) % (10**5)
        id = 90000000 + (hashed % 100000)

    if len(str(id)) != 8:
        id = 10000000 + int(id)
    return id


def findProductName(path: str):
    _path = Path(path)
    # find product name inside *Runtime\Support\*.dsx

    # get final part after last path seperator
    productName = _path.stem

    # remve IM#-# suffix IM0000-00_ABC -> _ABC
    thestring = re.sub(r"^IM\d+-\d+", "", productName)

    # remove more than 1 spaces
    thestring = re.sub(r" {2,}", " ", thestring)

    # remove daz prefixes
    daz_prefixes = []
    for pref1 in ["[daz]", "[DAZ]"]:
        for pref2 in ["", " ", " - ", "-", "- "]:
            daz_prefixes.append(pref1 + pref2)

    for prefix in daz_prefixes:
        if thestring.startswith(prefix):
            thestring = thestring.replace(prefix, "")

    thestring = thestring.strip()

    # remove sku ID
    thestring = re.sub(r"\d{5,}", "", thestring)

    # replace underscores with spaces
    thestring = thestring.replace("_", " ").strip()

    # add space between lowercaseUpperCase pairs: aB -> a B
    thestring = re.sub(r"([a-z])([A-Z])", r"\1 \2", thestring)

    return thestring


def findDsxName(productid, productnameNoSpaces):
    return "IM{:08d}-{:02d}_{}.dsx".format(productid, 0, productnameNoSpaces)


def findZipName(productid, productnameNoSpaces):
    return "IM{:08d}-{:02d}_{}.zip".format(productid, 0, productnameNoSpaces)


def findManifest(filelist):
    return any(
        [
            file.startswith("manifest.dsx") and file.casefold().endswith(".dsx")
            for file in filelist
        ]
    )


def validate_defaultDimStructure(filelist: list[str]):
    """validate the structure of the fililist to conform DazInstallManager requirements
    return true when root level contains:
      content/
      manifest.dsx
      supplement.dsx (optional)
      content/runtime/support/*.dsx
    """
    contentFolderName = "content/".casefold()

    posixFilelist = [str(Path(x).as_posix()) for x in filelist]
    filelist = [f.casefold() for f in posixFilelist]
    hasContent = any([contentFolderName in file for file in filelist])
    hasSupport = any(
        [
            file.startswith("content/runtime/support/".casefold())
            and file.casefold().endswith(".dsx")
            for file in filelist
        ]
    )
    hasManifest = findManifest(filelist)

    return hasContent and hasManifest#and hasSupport


def validate_defaultDazStructure(fileList: list[Path]):
    rootdirs = [
        "data",
        "Runtime",
        "People",
        "Scripts",
        "Shaders",
        "Presets",
        "Shader Presets",
        "Materials",
    ]

    rootdirs = [str(x).casefold() for x in rootdirs]
    fileList = [str(x).casefold() for x in fileList]

    for path in fileList:
        for rootdir in rootdirs:
            if path.startswith(rootdir):
                return True
    return False


def validate_containsContentFolder(filelist):
    filelist = [str(Path(x).as_posix()) for x in filelist]
    has = any(["Content/".casefold() in name.casefold() for name in filelist])
    return has


def findContentFolder(filelist: list[str]):
    contentFolders=[]

    for filepath in filelist:
        filepath=Path(filepath)
        casefolded=str(filepath.as_posix()).casefold()
        if "content/" in casefolded:
            contentFolders.append(filepath)
    commonpath=os.path.commonpath([str(x) for x in contentFolders])

    if "content/" in commonpath.casefold():
        return Path(commonpath).as_posix()

    if len(contentFolders)>0:
        return contentFolders[0].as_posix()[:str(casefolded).index("content/")+8]
    return None

class Archivedata:
    def __init__(self, archivePath: Path) -> None:
        self.path = archivePath
        self.isArchive = zipfile.is_zipfile(self.path)
        self.filelist = self.getfilelist()
        self.sourceType = self.validateSource()
        self.productID = findProductID(self.path)
        self.ProductName = findProductName(self.path)
        self.ProductNameNoSpaces = self.ProductName.replace(" ", "")
        self.DsxName = findDsxName(self.productID, self.ProductNameNoSpaces)
        self.zipname = findZipName(self.productID, self.ProductNameNoSpaces)
        self.destinationFolder = ""
        self.archiveHandler=None

    def as_archive(self) -> ZipFile:
        return ZipFile(self.path, "r")

    def as_folder(self) -> Path:
        return Path(self.path)

    def getfilelist(self):
        if self.isArchive:
            return [Path(name) for name in self.as_archive().namelist()]
        else:
            return [f.relative_to(self.path) for f in self.as_folder().rglob("*")]

    def getContentFolder(self):
        return findContentFolder(self.filelist)

    def getFinalZipPath(self):
        """the final path on the system where the generate .zip file will be saved"""
        thepath = Path(self.destinationFolder) / self.zipname
        return thepath


    def validateSource(self) -> mkdim_types.SourceType:
        hasManifest = "Manifest.dsx" in self.filelist
        is_defaultDimStructure = validate_defaultDimStructure(self.filelist)
        is_defaultDazStructure = validate_defaultDazStructure(self.filelist)
        hasContentFolder = validate_containsContentFolder(self.filelist)

        if is_defaultDazStructure:
            return mkdim_types.SourceType.DEFAULT_DAZ
        elif is_defaultDimStructure:
            return mkdim_types.SourceType.DEFAULT_DIM
        elif hasContentFolder and not hasManifest:
            return mkdim_types.SourceType.CONTAINTS_CONTENT_NO_MANIFEST
        elif hasContentFolder and hasManifest:
            return mkdim_types.SourceType.CONTAINTS_CONTENT_WITH_MANIFEST
        else:
            return mkdim_types.SourceType.INVALID
