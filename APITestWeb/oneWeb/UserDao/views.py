import hashlib
import logging
import os
import time

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.http import request,response
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#log
logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
logPath = os.path.join(BASE_DIR+'/webLog/','log.log')
handf = logging.FileHandler(logPath,mode='a')
handf.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
handf.setFormatter(formatter)
logger.addHandler(handf)
logger.debug("日志系统已启动！")


#登入登出---------------------------------
def logins(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if not user:
            return HttpResponse('<script>window.alert("账号不存在或密码错误！"); window.history.back(-1); </script>')
        else:
            login(request,user)
            path = request.GET.get("next") or "/upload/"
            # return redirect(path)
            return HttpResponse("<script>window.alert('登陆成功'); window.location.replace("+str(path)+"); </script>")
    else:
        return redirect("/login/")

@login_required
def logouts(request):
    logout(request)
    logger.info("退出登陆")
    return HttpResponse('<script>window.alert("退出成功！"); window.location.replace("/login/"); </script>')

@login_required
def index(request):
    return render(request,'upload.html')

#注册
def createUser(request):
    if request.method == 'GET':
        return redirect("/login/")
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_1 = request.POST.get("password-1")
        email = request.POST.get('email')
        try:
            u = User.objects.get(username=username)
        except Exception as e:
            u = None

        if username == None or username == '':
            return HttpResponse("<script>window.alert('用户名不能为空'); window.history.back(-1); </script>")
        elif password == None or password == '' :
            return HttpResponse("<script>window.alert('密码不能为空'); window.history.back(-1); </script>")
        elif password_1 == None or password_1 == '' :
            return HttpResponse("<script>window.alert('重复密码不能为空'); window.history.back(-1); </script>")
        elif email == None or email == '':
            return HttpResponse("<script>window.alert('邮箱不能为空'); window.history.back(-1); </script>")
        elif password != password_1:
            return HttpResponse("<script>window.alert('两次密码不一致！'); window.history.back(-1); </script>")
        elif u:
            return HttpResponse("<script>window.alert('用户名已注册！'); window.history.back(-1); </script>")
        else:
            userObj =  User.objects.create_user(username=username,email=email,password=password)
            if not userObj:
                return HttpResponse("<script>window.alert('注册失败!'); window.history.back(-1); </script>")
            else:
                return HttpResponse('<script>window.alert("注册成功！"); window.location.replace("/login/"); </script>')
    else:
        return redirect("/login/")

#重置密码
def remakePassword(request):
    if request.method == 'GET':
        return redirect('/login/')
    elif request.method == 'POST':
        username = request.POST.get('username')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        try:
            userObj = User.objects.get(username=username)
        except Exception as e:
            return HttpResponse("<script>window.alert('用户名不存在'); window.history.back(-1); </script>")
        if username == None or username == '':
            return HttpResponse("<script>window.alert('用户名不能为空'); window.history.back(-1); </script>")
        elif oldPassword == None or oldPassword == '':
            return HttpResponse("<script>window.alert('密码不能为空'); window.history.back(-1); </script>")
        elif newPassword == None or newPassword == '':
            return HttpResponse("<script>window.alert('新密码不能为空'); window.history.back(-1); </script>")
        elif not authenticate(username=username,password=oldPassword):
            return HttpResponse("<script>window.alert('密码错误'); window.history.back(-1); </script>")
        elif oldPassword == newPassword:
            return HttpResponse("<script>window.alert('新老密码不能重复！'); window.history.back(-1); </script>")
        else:
            userObj.set_password(newPassword)
            userObj.save()
            return HttpResponse('<script>window.alert("重置密码成功！"); window.location.replace("/login/"); </script>')
    else:
        return redirect('/login/')

#忘记密码
def forgetPassword(request):
    if request.method == 'GET':
        return redirect('/login/')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_1 = request.POST.get('password-1')
        try:
            userObj = User.objects.get(username=username)
        except Exception as e:
            return HttpResponse("<script>window.alert('用户名不存在'); window.history.back(-1); </script>")
        if username == None or username == '':
            return HttpResponse("<script>window.alert('用户名不能为空'); window.history.back(-1); </script>")
        elif email == None or email == '':
            return HttpResponse("<script>window.alert('邮箱不能为空'); window.history.back(-1); </script>")
        elif password == None or password == '':
            return HttpResponse("<script>window.alert('密码不能为空'); window.history.back(-1); </script>")
        elif password_1 == None or password_1 == '':
            return HttpResponse("<script>window.alert('重复密码不能为空'); window.history.back(-1); </script>")
        elif userObj.email != email:
            return HttpResponse("<script>window.alert('邮箱错误，请重新输入！'); window.history.back(-1); </script>")
        elif password != password_1:
            return HttpResponse("<script>window.alert('两次密码输入不一致！'); window.history.back(-1); </script>")
        else:
            userObj.set_password(password)
            userObj.save()
            return HttpResponse('<script>window.alert("找回密码成功！"); window.location.replace("/login/"); </script>')

    else:
        return redirect("/login/")
# ---------------------------------------



