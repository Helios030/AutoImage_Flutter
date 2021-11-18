import shutil
import subprocess
import time
import zipfile
from tkinter import filedialog
import os



def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


def get_last_line(inputfile):
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')

    last_line = b""
    lines = []
    if filesize > blocksize:
        maxseekpoint = (filesize // blocksize)  # 这里的除法取的是floor
        maxseekpoint -= 1
        dat_file.seek(maxseekpoint * blocksize)
        lines = dat_file.readlines()
        while ((len(lines) < 2) | ((len(lines) >= 2) & (lines[1] == b'\r\n'))):  # 因为在Windows下，所以是b'\r\n'
            # 如果列表长度小于2，或者虽然长度大于等于2，但第二个元素却还是空行
            # 如果跳出循环，那么lines长度大于等于2，且第二个元素肯定是完整的行
            maxseekpoint -= 1
            dat_file.seek(maxseekpoint * blocksize)
            lines = dat_file.readlines()
    elif filesize:  # 文件大小不为空
        dat_file.seek(0, 0)
        lines = dat_file.readlines()
    if lines:  # 列表不为空
        for i in range(len(lines) - 1, -1, -1):
            last_line = lines[i].strip()
            if (last_line != b''):
                break  # 已经找到最后一个不是空行的
    dat_file.close()
    return last_line


def addImage(answerDir):
    unzipDir = os.path.dirname(answerDir) + "/" + str(time.time())
    unzip_file(answerDir, unzipDir)
    list = os.listdir(unzipDir)
    # 取出映射关系

    nameList = []
    for value in list:
        nameList.append(value.split("@")[0])
    for name in set(nameList):
        filename = input("请输入 " + name + " 的文件名：")
        allFileName = filename + ".png"
        imgDir2List = os.listdir(imgDir2)
        if allFileName in imgDir2List:
            print("文件已存在 ！！ " + name + "@2x.png")
        else:
            shutil.copy(os.path.join(unzipDir, name + "@2x.png"), os.path.join(imgDir2, allFileName))
            shutil.copy(os.path.join(unzipDir, name + "@3x.png"), os.path.join(imgDir3, allFileName))
            print("文件复制完成")
            print("开始写入yaml。。。")
            rfile.write("String n" + allFileName.split(".")[0] + "= \"assets/images/" + allFileName + "\";\n")
            with open(yamiuri, 'a+') as f:
                lastline = get_last_line(yamiuri)
                if (str(lastline).__contains__("uses-material-design")):
                    f.write("\nassets:")
                    f.write("\n - assets/images/" + allFileName)
                else:
                    f.write("\n - assets/images/" + allFileName)
            print("yaml写入完毕")
    print("图片添加完毕！")
    print("删除文件中。。。")
    os.remove(answerDir)
    shutil.rmtree(unzipDir)
    print("删除文件完毕")
    print("运行 Flutter get")
    subprocess.Popen('/Users/ben/Work/flutter/bin/flutter --no-color pub get', shell=True, cwd=projectDir)
    print("运行完毕   ")

projectDir = "/Users/ben/Work/StudioProjects/philippines_loan"
yamiuri = projectDir + "/pubspec.yaml"
rfile = open(projectDir+"/lib/resource.dart",'a+')




imgDir2 = projectDir + "/assets/images/2.0"
imgDir3 = projectDir + "/assets/images/3.0"

if not os.path.exists(imgDir2):
    os.makedirs(imgDir2)
    os.makedirs(imgDir3)
# 设置文件对话框会显示的文件类型


model = input("""
请输入工作模式：
1.选择压缩文件添加
2.自动监听下载目录有新的压缩文件添加
3.生成R类


""")
answerDir = ""
downloadDir="/Users/ben/Downloads"
if model == "1":
    filetypes = [('zip files', '.zip')]
    # 请求选择文件
    answerDir = filedialog.askopenfilename(initialdir=os.getcwd(), title="选择蓝湖下载压缩包:",
                                           filetypes=filetypes)
    addImage(answerDir)
else :
    if model == "2":
        lastTime = 0.0;
        while 1 == 1:
            dirTime = os.path.getmtime(downloadDir)
            if dirTime > lastTime:
                lastTime = dirTime
                dirlists = os.listdir(downloadDir)
                newlist = []
                for value in dirlists:
                    if "zip" in value:
                        newlist.append(value)

                newlist.sort(key=lambda fn: os.path.getmtime(downloadDir + "/" + fn))  # 按时间排序
                print("最新文件  " + str(newlist[-1]))
                addImage(downloadDir + "/" + newlist[-1])
                input("输入任意键继续监听。。。。。")
            else:
                time.sleep(50000)
    else:
        imglists = os.listdir(imgDir2)
        for img in imglists:
            imgName=img.split(".")[0]
            rfile.write("String n"+imgName+"= \"assets/images/"+img+"\";\n")



