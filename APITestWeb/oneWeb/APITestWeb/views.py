#coding:utf-8

import os
import shutil
import time
import zipfile,threading
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
import logging

# Create your views here.
from APITest.Run import getRun
from django.utils.encoding import escape_uri_path
from django.contrib.auth.decorators import login_required


from APITestWeb.models import TestCasePath


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #oneWeb
FBASE_DIR = os.path.abspath(os.path.dirname(os.getcwd()))  #git


codePath = '/usr/testcase/TestCase'
casePath = '/usr/testcase/TestCase'

# codePath = 'D:/ONE'
# casePath = 'D:/ONE'



#log
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logPath = os.path.join(BASE_DIR+'/webLog/','log.log')
handf = logging.FileHandler(logPath,mode='a')
handf.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
handf.setFormatter(formatter)
logger.addHandler(handf)

logger.debug("日志系统已启动！")

logger.debug("当前路径："+str(BASE_DIR))




def checkLog():
    try:
        file = os.path.join(BASE_DIR+'/webLog/','log.log')
        fileSize = os.path.getsize(file)
        if fileSize >= 1024*1024*20:
            fileNew = os.path.join(BASE_DIR+'/webLog/','log'+str(int(time.time()))+'.log')
            with open(fileNew,'w') as f:
                mycopyfile(BASE_DIR + '/webLog/log.log', BASE_DIR + "/LOG")
                with open(BASE_DIR + '/webLog/log.log', 'w') as f:
                    f.close()
                    logger.debug("清理日志完成！")
    except Exception as e:
        logger.debug("清理日志失败!")

checkLog()
logger.debug("启动检测日志程序")

def delFiles(fpath):
    try:
        if not os.path.isdir(fpath):
            logger.debug("请确认输入的是正确的路径！")
        else:
            dataList = os.listdir(fpath)
            for i in dataList:
                f = os.path.join(fpath,i)
                if os.path.isdir(f):
                    os.rmdir(f)
                elif os.path.isfile(f):
                    os.remove(f)
                else:
                    logger.debug(str(f)+'无法识别文件！')
    except Exception as e:
        logger.debug('删除文件失败： '+str(e))

def mycopyfile(srcfile,dstpath):                       # 移动函数
    if not os.path.isfile(srcfile):
        logger.debug ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        fileList = os.listdir(dstpath)
        p = fname.split('.')[0]
        typ = fname.split('.')[-1]
        k = 1
        while fname in fileList:
            fname = p + '(' + str(k) + ').' + typ
            k += 1
        shutil.copy(srcfile, dstpath + fname)          # 移动文件
        logger.debug ("move %s -> %s"%(srcfile, dstpath + fname))

@login_required
def getCodeFile(request):
    try:
        if request.method == 'POST':
            myFile = request.FILES.get('code_file', None)
            if not myFile:
                return redirect("/upload/")  # home page should with error
            fileList = os.listdir(codePath)
            fileName = myFile.name
            p = myFile.name.split('.')[0]
            typ = myFile.name.split('.')[-1]
            k = 1
            while fileName in fileList:
                fileName = p + '(' + str(k) + ').' + typ
                k += 1
            destination = open(
                os.path.join(codePath, fileName), 'wb+')

            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()


            return redirect('/upload/')

        else:
            return redirect('/upload/')
    except Exception as e:
        logger.debug("处理文件失败："+str(e))

@login_required
def upload(request):
    if request.method == 'GET':
        checkLog()
        logger.debug("启动检测日志程序")
        userObj = request.user
        nameList_1 = []
        nameList_0 = []

        fileData = TestCasePath.objects.filter(user=userObj)

        for i in list(fileData):
            type = int(i.type)
            if type == 1:
                name = i.name
                nameList_1.append(name)
            elif type == 0:
                name = i.name
                nameList_0.append(name)

        context = {
            "MkdirData": nameList_0, 'codeFile': nameList_1,'username':userObj.username
        }
        logger.debug(str(context))
        return render(request, 'upload.html', context)
    elif request.method == "POST":
        myFile = request.FILES.get('upload_file', None)
        if not myFile:
            return HttpResponse("<script>window.alert('请上传文件!'); window.history.back(-1); </script>")  # home page should with error
        fileList = os.listdir(casePath)
        fileName = myFile.name
        p = myFile.name.split('.')[0]
        typ = myFile.name.split('.')[-1]
        k = 1
        while fileName in fileList:
            fileName = p+'('+str(k)+').'+typ
            k+=1
        destination = open(os.path.join(casePath, fileName), 'wb+')

        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        name = request.POST.get('name')
        if name == '' or name == None:
            return HttpResponse("<script>window.alert('名称不可为空!'); window.history.back(-1); </script>")

        #检测名称不可重复
        data = TestCasePath.objects.filter()
        for p in data:
            if p.name==name:
                return HttpResponse("<script>window.alert('名称已存在！'); window.history.back(-1); </script>")

        filePath = fileName
        type = int(request.POST.get('type'))
        userObj = request.user
        t = TestCasePath.objects.create(name=name,filePath=filePath,type=type,user=userObj)
        t.save()

        return redirect('/upload/')

    else:
        redirect('/upload/')


lock = threading.Lock()
@login_required
def RunTestCase(request):
    if request.method == 'GET':
        while True:
            try:
                #启动程序
                filename = request.GET.get('filename')

                p = TestCasePath.objects.filter(name=filename)[0]

                filePath =os.path.join(casePath, p.filePath)
                lock.acquire()
                logger.debug("用例名：{0} 开始执行操作。。".format(str(filename)))
                end = getRun(filePath)
                if end == 1:
                    result = '启动成功！'
                else:
                    result = '启动失败！'
                logger.debug("执行完毕，处理日志中。。")
                with open(BASE_DIR + '/APITest/log/logging.log', 'r') as f:
                    log = f.readlines()
                    f.close()



                userObj = request.user
                nameList_1 = []
                fileData = TestCasePath.objects.filter(user=userObj)

                for i in list(fileData):
                    type = int(i.type)
                    if type == 1:
                        name = i.name
                        nameList_1.append(name)


                mycopyfile(BASE_DIR + '/APITest/log/logging.log', BASE_DIR + "/APITest/LOGZIP/")

                with open(BASE_DIR + '/APITest/log/logging.log', 'w') as f:
                    f.close()
                content = {'codeFile':nameList_1,'log':log,'result':result,'filename':filename}
                time.sleep(1)
                lock.release()
                logger.debug("处理文件{0}结束，返回数据{1}".format(str(filename), str(content)))
                return render(request,'result.html',content)
            except Exception as e:
                logger.debug("程序等待中。。",e)
                redirect('/upload/')
    else:
        redirect("/upload/")



@login_required
def download_template(request):
    resultFile = open(BASE_DIR + "/APITest/模板.xlsx", 'rb')

    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path("demo.xlsx"))
    return response

@login_required
def download_user(request):
    resultFile = open(BASE_DIR + "/APITest/接口自动化操作手册.docx", 'rb')

    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path("接口自动化使用手册.docx"))

    return response

@login_required
def download_report(request):
    name = request.GET.get('filename')
    fileName = TestCasePath.objects.filter(name=name)[0].filePath
    resultFile = open(casePath+'/'+fileName, 'rb')

    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path(fileName))

    return response


@login_required
def download_code(request):
    name = request.GET.get('fn')
    data = TestCasePath.objects.filter(name=name)[0]
    filename = data.filePath
    resultFile = open(codePath+'/'+filename, 'rb')
    response = FileResponse(resultFile)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path(filename))

    return response

