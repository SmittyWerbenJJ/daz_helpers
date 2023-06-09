
import os
from pathlib import Path
import shutil
from zipfile import ZipFile
from . import progressReport,ziputils
from .mkdim_types import SourceType
from .archivedata import Archivedata
from .manifest import Manifest
from .supplement import Supplement
import tempfile
def clearFolder(folder:Path):
    for file_path in folder.iterdir():
        try:
            if file_path.is_file() or file_path.is_symlink():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)
        except Exception as e:
            raise Exception('Failed to delete %s. Reason: %s' % (file_path, e))

def removeFolder(folder:Path):
    try:
        os.system(f"rmdir /s /q {folder}")
    except Exception as e:
        print(e)

def getNewTenpDir():
    return Path(tempfile.mkdtemp())
class Archive:
    def __init__(self, archivePath: Path) -> None:
        self.source = Archivedata(archivePath)
        self.setDestinationFolder("")

    def setDestinationFolder(self, destinationFolder: str):
        destinationFolder = str(destinationFolder).strip()
        if destinationFolder != "":
            p_folder = Path(destinationFolder)
            try:
                p_folder.mkdir(exist_ok=True, parents=True)
            except:
                pass

            if os.path.exists(p_folder):
                self.source.destinationFolder = p_folder
                return
        self.source.destinationFolder = Path(self.source.path).parent

    def writeFilesToArchive(self,manifest:Manifest):
        """\
        - extract/move files to temp dir
        - pack the whole temp dir with new name
        - clear temp dir
        """
        tempdir=getNewTenpDir()
        tmpdir_extract=tempdir.joinpath("extract")
        tmpdir_packme=tempdir.joinpath("packme")
        for folder in [tmpdir_packme,tmpdir_extract]:
            folder.mkdir(parents=True,exist_ok=True)

        #add support/manifest dsx files
        tmpdir_packme.joinpath("Supplement.dsx").write_text(Supplement(self.source.ProductName).toString())
        tmpdir_packme.joinpath("Manifest.dsx").write_text(manifest.toString())

        if self.source.isArchive:
            #extract the archives to tmpdir
            ziputils.extractWith7zip(self.source.path,tmpdir_extract)
        else:
            #copy folder content to tmpdir
            for entry in manifest.entries:
                _from=self.source.path.joinpath(entry.sourcePath)
                _to=tmpdir_extract.joinpath(entry.sourcePath)
                _to.parent.mkdir(exist_ok=True,parents=True)
                shutil.copy(str(_from),str(_to))

        # before packing, modify extracted files -move files to packdir and rename according to manifest
        # also rename promo image
        for entry in manifest.entries:
            _from=tmpdir_extract.joinpath(entry.sourcePath)
            _to=tmpdir_packme.joinpath(entry.manifestPath)
            _to.parent.mkdir(parents=True,exist_ok=True)
            shutil.move(str(_from),str(_to))

        ziputils.createZipfileWith7zip(tmpdir_packme,self.source.getFinalZipPath())
        removeFolder(tempdir)

    def processArchive(self, destinationFolder="", callback_report=None):
        if callback_report is None:
            callback_report = lambda x: None

        callback_report(
            progressReport.ProgressReport(
                f"Processing {Path(self.source.path).name} ..."
            ).setMessageType(progressReport.MessageType.INFO)
        )

        self.setDestinationFolder(destinationFolder)
        match=self.source.sourceType
        if match==SourceType.DEFAULT_DIM:
                self.handleDefaultDIM(callback_report)
        elif match== SourceType.DEFAULT_DAZ:
                self.handleDefaultDAZ(callback_report)

        elif match==SourceType.CONTAINTS_CONTENT_NO_MANIFEST:
                self.handleContainsContentNoManifest(callback_report)
                return SourceType.CONTAINS_CONTENT

        elif match== SourceType.CONTAINTS_CONTENT_WITH_MANIFEST:
                self.handleContainsContentWithManifest(callback_report)
                return SourceType.CONTAINS_CONTENT

        return match

    def handleContainsContentWithManifest(self, callback_report):
        # archive has manifest, content folder is in some subdirectory -> put files content folder and manifest in root of new Archive
        self.handleContainsContentWithManifest(callback_report)
        return
        message = f"[NOT IMPLEMENTED] ArchiveType.CONTAINTS_CONTENT_AND_MANIFEST for {self.source.path}"
        callback_report(
            progressReport.ProgressReport(message).setMessageType(
                progressReport.MessageType.INFO
            )
        )

    def handleContainsContentNoManifest(self, callback_report):
        """archive has no Manifest, content folder is in some subdirectory -> put files from sub-content folders,create manifest and support images"""

        print("handleContainsContentNoManifest")
        contentFolder = self.source.getContentFolder()
        # skip if content folders do not contain  daz root paths
        if contentFolder is None:
            return progressReport.ProgressReport(
                f"{self.source.path} does not contain valid daz folders!"
            ).setMessageType(progressReport.MessageType.ERROR)

        manifest=Manifest(self.source.filelist,self.source.productID,self.source.ProductName)
        self.writeFilesToArchive(manifest)

    def handleDefaultDAZ(self, callback_report):
        """source has valid daz root paths, put files in content folder,create manifest and support images"""
        manifest=Manifest(self.source.filelist,self.source.productID,self.source.ProductName)
        self.writeFilesToArchive(manifest)

    def handleDefaultDIM(self, callback_report):
        """source is already dim, copy and rename / pack and rename"""
        _from = self.source.path
        _to = self.source.getFinalZipPath()
        if self.source.isArchive:
            if str(_from) != str(_to):
                shutil.copy(_from, _to)
        else:
            ziputils.createZipfile(_from, _to)
