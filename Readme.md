A small suite of tools for working with Daz files

---
### mkdim
This tool allows you to Pack files for use with the [Daz Install manager (DIM)](https://www.daz3d.com/install-manager-info).
You can drag&drop folders and archives(.zip files) in the ui and the tool will create IM-Files for you.
Your files should have one of the following file structures:
```
C:\path\to\my\folder\myProduct12345
or
C:\path\to\my\zipfile\myProduct12345.zip
```
inside the folder or the .zip file, the structure should be one of those:
```
\content\data\whatever\...
\content\people\whatever\...
\myCoolProduct\Content\runtime\whatever\...
\my\weirdly\packaged\product\content\data\whatever\...
\data\people\DAZ 3D\whatever\...
\people\Genesis X\whatever\...
```
Promo images of your product that you put in root- or the contentfolder, will be used as thumbnails inside daz studio

---
### Extract parents
This tool will give you the parent paths of any given file/folder paths. You also can open the results in [Everything](https://www.voidtools.com/), or  them to the clipboard


---
### building

To Build the Executable  
create a conda environment with ```conda create --prefix=.\.conda```  
install pip requirements ```pip install -r requirements.txt```  
run the batch file ```build.bat```
