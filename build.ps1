pyinstaller.exe -F -w -n PavlovToolbox `
-i "icon.ico" `
--add-data "icon.ico:." `
--add-data "aria2/aria2.conf:aria2" `
--add-data "aria2/aria2c.exe:aria2" `
.\main.py