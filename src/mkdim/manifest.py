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


def getImageSuffixes():
    return [
    ".tga",".png",".bmp",".jpg",".jpeg",".webm"
    ]
class ManifestEntry:
    def __init__(self, sourcePath:Path, manifestPath:Path) -> None:
        self.sourcePath = sourcePath
        self.manifestPath = manifestPath

class Manifest:
    header = '<DAZInstallManifest VERSION="0.1">'
    id_template='<GlobalID VALUE="{}" />'
    content_template='\t<File TARGET="Content" ACTION="Install" VALUE="{}" />'
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
            match= re.match(r"(^.*)(content\/)(.*)",file.as_posix(),re.RegexFlag.IGNORECASE)

            if match:
                manifestpath=Path("C"+(match.group(2)+match.group(3))[1:])
            elif file.name in getRootDirs():
                manifestpath=Path("Content/"+file.as_posix())
            elif file.suffix in getImageSuffixes():
                self.addPromoImage(file)
                continue
            else:
                continue

            if manifestpath.suffix==(""):
                continue

            self.addEntry(file,Path(manifestpath))

        # self.entries.sort(key=lambda x: len(x.manifestPath.as_posix()))

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
            lines.append(self.content_template.format(entry.manifestPath))
        lines.append(self.footer)
        return "\n".join(lines)
