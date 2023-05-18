rd "C:\Users\Дом\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe" /S /Q

"C:\Users\Дом\PycharmProjects\Hungarian Rings\venv\Scripts\pyinstaller" main.py -n "Hungarian Rings.exe" -i "Hungarian Rings.ico" --onedir --noconsole --splash "splashfile.gif" --upx-dir C:\Users\Дом\PycharmProjects\UPX

copy "C:\Users\Дом\PycharmProjects\Hungarian Rings\Hungarian Rings.png" "C:\Users\Дом\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe"
copy "C:\Users\Дом\PycharmProjects\Hungarian Rings\README.txt" "C:\Users\Дом\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe"

md "C:\Users\Дом\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Rings"
md "C:\Users\Дом\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Samples"
copy "C:\Users\Дом\PycharmProjects\Hungarian Rings\Rings\*.*" "C:\Users\Дом\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Rings"
copy "C:\Users\Дом\PycharmProjects\Hungarian Rings\Samples\*.*" "C:\Users\Дом\PycharmProjects\Hungarian Rings\dist\Hungarian Rings.exe\Samples"
