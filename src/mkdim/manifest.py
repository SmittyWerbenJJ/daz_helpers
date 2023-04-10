from pathlib import Path
from . import ziputils
import re
import uuid
import hashlib

def getRootDirs():
    dirs = [
        "data",
        "Runtime",
        "People",
        "Scripts",
        "Shaders",
        "Presets",
        "Shader Presets",
        "Materials",
    ]
    return  [str(x).casefold() for x in dirs]

def fix_xml_reference(string):
   return string.replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("&","&amp;").replace("'","&apos;")

def getImageSuffixes():
    return [
    ".tga",".png",".bmp",".jpg",".jpeg",".webm"
    ]

def findRootpath(path:Path):
    for rootdir in getRootDirs():
        idx = path.as_posix().casefold().find(rootdir)
        if idx!=-1:
            return (idx,rootdir)
    return (-1,None)



class ManifestEntry:
    def __init__(self, sourcePath:Path, manifestPath:Path) -> None:
        self.sourcePath = sourcePath
        self.manifestPath = Path(manifestPath.as_posix().lstrip("/"))

class Manifest:
    header = '<DAZInstallManifest VERSION="0.1">'
    id_template='<GlobalID VALUE="{}" />'
    content_template='  <File TARGET="Content" ACTION="Install" VALUE="{}" />'
    footer='</DAZInstallManifest>'
    supportDir=Path("Content/Runtime/Support/")

    def __init__(self,filelist:list[Path],productID:int,productName:str) -> None:
        self.id=productID
        self.filelist=filelist
        self.entries:list[ManifestEntry] = []
        self.promoImage =None
        self.productName=productName

        #create manifest from source
        for file in filelist:
            #find content folder
            contentPath=Manifest.makeContentPath(file)
            rootDirPath=Manifest.makeRootDirPath(file)
            promoImgPath=self.makePromoImgPath(file)
            if contentPath:
                manifestpath=contentPath
            elif rootDirPath:
                manifestpath=rootDirPath
            elif promoImgPath and not self.promoImage:
                #can this path be used as promo img?
                manifestpath=promoImgPath
                self.promoImage=promoImgPath
            else:
                continue

            if Manifest.isFileDirectory(file,filelist):
                continue


            self.addEntry(file,Path(manifestpath))

    def isFileDirectory(file:Path,filelist:list[Path]):
        strfile=file.as_posix()
        for other in [x.as_posix() for x in filelist]:
            idx= other.find(strfile+"/")
            if idx>=0:
                return True
        return False

    def makeContentPath(file:Path):
        posixpath=file.as_posix().casefold()
        idx=posixpath.rfind("content/")
        if idx!=-1:
            return Path(file.as_posix()[idx:])
        return None

    def makeRootDirPath(file):
        posixpath=file.as_posix().casefold()
        for rootdir in getRootDirs():
            idx = posixpath.find(rootdir)
            if idx!=-1:
                return Path("Content/"+file.as_posix()[idx:])
        return None


    def makePromoImgPath(self,file:Path):
        if file.suffix.casefold() in getImageSuffixes():
            return Manifest.supportDir.joinpath(Path(self.productName).with_suffix(file.suffix))
        return None

    def addEntry(self, sourcePath, mainfestpath):
        entry=ManifestEntry(sourcePath, mainfestpath)
        self.entries.append(entry)
        return entry

    def findProductImage(self,productName:str):
        """detect Promo Image and place in right folder"""
        #todo check if supportdir already contains Promo Image
        if self.promoImage!=None :
            return self.promoImage.sourcePath

        for entry in self.entries:
            # if entry.manifestPath.parent.as_posix() =="Content/":
            if( len(entry.manifestPath.parents)<3 and
             entry.sourcePath.suffix in [".tga",".png",".bmp",".jpg",".jpeg",".webm"]):
                entry.manifestPath=Manifest.supportDir.joinpath(productName).with_suffix(entry.sourcePath.suffix)
                self.promoImage=entry
                return self.promoImage.sourcePath

    def addPromoImage(self,sourcepath:Path):
        promoImgPathManifest=self.supportDir.joinpath(self.productName).with_suffix(sourcepath.suffix)
        if self.promoImage is None:
            entry=self.addEntry(sourcepath,promoImgPathManifest)
            self.promoImage=entry

        return self.promoImage.manifestPath

    def toString(self):
        "B62ED1BE-5627-47E4-84AA-34BF4C95CB81"
        m = hashlib.md5()
        m.update(str(self.id).encode("utf8"))
        guid = uuid.UUID(m.hexdigest())
        lines=[self.header,self.id_template.format(guid)]

        for entry in self.entries:
            lines.append(self.content_template.format(fix_xml_reference(entry.manifestPath.as_posix())))
        lines.append(self.footer)
        return "\n".join(lines)
