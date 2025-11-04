rd "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe" /S /Q

"D:\PycharmProjects\Hungarian Rings\venv8\Scripts\pyinstaller" main.py -n "Hungarian Rings.exe" -i "Hungarian Rings.ico" --onedir --noconsole --splash "splashfile.gif" --upx-dir D:\PycharmProjects\UPX

copy "D:\PycharmProjects\Hungarian Rings\Hungarian Rings.png" "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\"
copy "D:\PycharmProjects\Hungarian Rings\README.txt" "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\"

md "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Rings"
md "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Photo"
md "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Samples"
xcopy "D:\PycharmProjects\Hungarian Rings\Rings\*.*" "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Rings" /S /E /Y /Q
xcopy "D:\PycharmProjects\Hungarian Rings\Photo\*.*" "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Photo" /S /E /Y /Q
xcopy "D:\PycharmProjects\Hungarian Rings\Samples\*.*" "D:\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Samples" /S /E /Y /Q
