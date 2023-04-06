call conda activate ./.conda
pyinstaller ^
--noconfirm ^
--onefile ^
--noconsole ^
--icon="icons/icon.ico" ^
--name="DAZ Helpers" ^
-y ^
"app.py"
