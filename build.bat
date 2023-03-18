call conda activate ./.conda
pyinstaller ^
--noconfirm ^
--onedir --windowed ^
--icon "src/icons/icon.ico" ^
--paths .conda/Lib/site-packages ^
--name "Extract Parents" ^
"cli.py"
