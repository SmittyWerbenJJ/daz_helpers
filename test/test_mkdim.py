import os
from pathlib import Path
import unittest
from src import mkdim
import shutil
from zipfile import ZipFile


def getTestFile(folder:Path):
    return list(folder.iterdir())[0]

class MkdimTest(unittest.TestCase):

    def setUp(self) -> None:
        """ Find test files and create test results folder"""
        self.testfolder=Path("test/data").absolute()

        self.testdir_archive_default_daz=self.testfolder/"archives/default DAZ"
        self.testdir_archive_default_daz_content=self.testfolder/"archives/default DAZ - Content"
        self.testdir_archive_default_daz_content_subdirectories=self.testfolder/"archives/default DAZ - Content - subdirectories"
        self.testdir_archive_default_dim=self.testfolder/"archives/default dim"
        self.testdir_archive_default_dim_subdirectories=self.testfolder/"archives/default dim - subdirectories"

        self.testdir_folder_default_daz=self.testfolder/"folders\default DAZ"
        self.testdir_folder_default_daz_content=self.testfolder/"folders\default DAZ - Content"
        self.testdir_folder_default_daz_content_subdirectories=self.testfolder/"folders\default DIM - Content - subdirectories"
        self.testdir_folder_default_dim=self.testfolder/"folders\default dim"

        self.testResultFolder=self.testfolder/"target folder"
        self.createdTestFiles:list[Path]=[]
        self.createdTestFolders=[self.testResultFolder]
        self.testResultFolder.mkdir(parents=True,exist_ok=True)

    # DefaultDIM
    def test_handleArchive_as_DefaultDIM_in_Subdirectory(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.DEFAULT_DIM,
            self.testdir_archive_default_dim,
            self.testResultFolder
            )
        )

    def test_handleArchive_as_DefaultDIM_in_parentDir(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.DEFAULT_DIM,
            self.testdir_archive_default_dim
            )
        )

    def test_handleArchive_as_DefaultDAZ_with_Content_in_Subdirectory(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_archive_default_daz_content,
            self.testResultFolder
            )
        )

    def test_handleArchive_as_DefaultDAZ_with_Content_in_parentDir(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_archive_default_daz_content,
            )
        )

    def test_handleArchive_as_DefaultDAZ_with_ContentSubdir_in_Subdirectory(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_archive_default_daz_content_subdirectories,
            self.testResultFolder
            )
        )

    def test_handleArchive_as_DefaultDAZ_with_ContentSubdir_in_parentDir(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_archive_default_daz_content_subdirectories,
            )
        )

    def test_handleFolder_as_DefaultDIM_in_Subdirectory(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.DEFAULT_DIM,
            self.testdir_folder_default_dim,
            self.testResultFolder
            )
        )

    def test_handleFolder_as_DefaultDIM_in_parentDir(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.DEFAULT_DIM,
            self.testdir_folder_default_dim
            )
        )

    def test_handleFolder_as_DefaultDAZ_in_Subdirectory(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.DEFAULT_DAZ,
            self.testdir_folder_default_daz,
            self.testResultFolder
            )
        )

    def test_handleFolder_as_DefaultDAZ_in_parentDir(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.DEFAULT_DAZ,
            self.testdir_folder_default_daz,
            )
        )

    def test_handleFolder_as_DefaultDAZ_with_Content_in_Subdirectory(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_folder_default_daz_content,
            self.testResultFolder
            )
        )

    def test_handleFolder_as_DefaultDAZ__with_Content_in_parentDir(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_folder_default_daz_content,
            )
        )

    def test_handleFolder_as_DefaultDAZ_with_ContentSubdir_in_Subdirectory(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_folder_default_daz_content_subdirectories,
            self.testResultFolder
            )
        )

    def test_handleFolder_as_DefaultDAZ_with_ContentSubdir_in_parentDir(self):
        self.assertTrue(
            self.RunGenericTest(
            mkdim.SourceType.CONTAINS_CONTENT,
            self.testdir_folder_default_daz_content_subdirectories,
            )
        )

    def RunGenericTest(self,sourceType:mkdim.SourceType,testfile:Path,resultsFolder:Path=""):
        _testfile=getTestFile(testfile)
        archive=mkdim.Archive(_testfile)
        _sourceType=archive.processArchive(resultsFolder)

        target_parent_folder=resultsFolder if resultsFolder !="" else _testfile.parent
        created_archive_path=target_parent_folder/archive.source.getFinalZipPath().name
        self.createdTestFiles.append(created_archive_path)
        if _sourceType !=sourceType:
            raise TypeError(f"Source type is not recognized as {sourceType.name}")
        return created_archive_path.exists()

    def tearDown(self) -> None:
        """remove generated files and folders"""
        for file in self.createdTestFiles:
            try: os.remove(file)
            except:pass
        for folder in self.createdTestFolders:
            shutil.rmtree(folder)




#     create_zip_mock.assert_called_once_with("source_path", "final_zip_path")

# def test_handleDefaultDAZ(mocker):
#     source_mock = MagicMock()
#     source_mock.getFinalZipPath.return_value = "final_zip_path"
#     source_mock.path = "source_path"
#     source_mock.ProductName = "product_name"

#     create_manifest_mock = mocker.patch("your_module.createManifest")
#     create_manifest_mock.return_value = ["manifest_line"]

#     with mocker.patch("zipfile.ZipFile") as zip_mock:
#         InputArchive.handleDefaultDAZ(None, source_mock, None)

#         create_manifest_mock.assert_called_once_with("source_path", zip_mock.return_value)
#         zip_mock.return_value.writestr.assert_any_call("Supplement.dsx", "supplement.format(product_name)")
#         zip_mock.return_value.writestr.assert_any_call("Manifest.dsx", "manifest_line\n")

# def test_handleContainsContentNoManifest(mocker):
#     source_mock = MagicMock()
#     source_mock.filelist = ["file1", "file2"]
#     source_mock.getFinalZipPath.return_value = "final_zip_path"
#     source_mock.path = "source_path"
#     source_mock.ProductName = "product_name"

#     find_content_mock = mocker.patch("your_module.findContentFolder")
#     find_content_mock.return_value = "content_folder"

#     create_manifest_reparent_mock = mocker.patch("your_module.createManifest_reparent")
#     create_manifest_reparent_mock.return_value = ["manifest_line"]

#     with mocker.patch("zipfile.ZipFile") as zip_mock:
#         InputArchive.handleContainsContentNoManifest(None, source_mock, None)

#         create_manifest_reparent_mock.assert_called_once_with("source_path", zip_mock.return_value, ["file1", "file2"], "content_folder")
#         zip_mock.return_value.writestr.assert_any_call("Supplement.dsx", "supplement.format(product_name)")
#         zip_mock.return_value.writestr.assert_any_call("Manifest.dsx", "manifest_line\n")

# def test_handleContainsContentNoManifest_error(mocker):
#     source_mock = MagicMock()
#     source_mock.filelist = ["file1", "file2"]
#     source_mock.getFinalZipPath.return_value = "final_zip_path"
#     source_mock.path = "source_path"

#     find_content_mock = mocker.patch("your_module.findContentFolder")
#     find_content_mock.return_value = None

#     callback_report = MagicMock()

#     InputArchive.handleContainsContentNoManifest(None, source_mock, callback_report)

#     callback_report.assert_called_once_with(("ERROR", "source_path does not contain valid daz folders!"))


if __name__ == "__main__":

    unittest.main()
