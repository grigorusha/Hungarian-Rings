rd "C:\Users\���\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe" /S /Q

"C:\Users\���\PycharmProjects\Hungarian Rings\venv\Scripts\pyinstaller" main.py -n "Hungarian Rings.exe" -i "Hungarian Rings.ico" --onedir --noconsole --splash "splashfile.gif" --upx-dir C:\Users\���\PycharmProjects\UPX

copy "C:\Users\���\PycharmProjects\Hungarian Rings\Hungarian Rings.png" "C:\Users\���\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe"
copy "C:\Users\���\PycharmProjects\Hungarian Rings\README.txt" "C:\Users\���\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe"

md "C:\Users\���\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Rings"
md "C:\Users\���\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Samples"
copy "C:\Users\���\PycharmProjects\Hungarian Rings\Rings\*.*" "C:\Users\���\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Rings"
copy "C:\Users\���\PycharmProjects\Hungarian Rings\Samples\*.*" "C:\Users\���\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Samples"
