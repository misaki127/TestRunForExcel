#coding:utf-8
#author:wanghan
import json
import re,time,openpyxl
from itertools import groupby
from json.decoder import JSONDecodeError

import chardet,requests


from APITest.common.con_Mysql import con_Mysql
from APITest.common.LoggerObj import *
from APITest.common.globeObj import *

from APITest.common import globeObj

def getFileCoding(filePath):
    try:
        # 获取文件编码格式

        with open(filePath, 'rb') as f:
            data = f.read()
            codingName = chardet.detect(data).get('encoding')
        return codingName
    except Exception as e:
        logging.info("获取文件编码格式失败：" + str(e)+'\n')

def splitCode(dataType,data,dataTypeSep,dataSep):  # 请求方式以逗号分隔，请求参数以分隔符分隔 将请求方式与参数一一配对组合在一起，组成一个str
    try:
        if data == "" or data == None or dataType == '' or dataType == None:
            return None
        dataType = dataType.strip()
        data = data.strip()
        methodList = dataType.split(dataTypeSep)
        dataList = data.split(dataSep)
        if len(methodList) != len(dataList):
            logging.info('请求方式与请求参数不匹配，请核对后重试'+'\n')
            result = None
        elif len(methodList) == 1 and methodList[0] == '':
            result = ''
        else:
            result = ''
            for a in range(len(methodList)):
                result += methodList[a] + '=' + dataList[a] + ','
        return result
    except Exception as e:

        logging.info('拼接代码：splitCode:' + str(e)+'\n')

def getResponse(url, method, **kwargs):

    # """封装request方法"""
    # # 获取请求参数
    params = kwargs.get("params")
    data = kwargs.get("data")
    json = kwargs.get("json")
    headers = kwargs.get('headers')
    cookies = kwargs.get('cookies')
    files = kwargs.get('files')  # {name ,(filename,fileobj,'content_type', custom_headers) }
    auth = kwargs.get('auth')  # 自定义身份验证
    timeout = kwargs.get('timeout')  # 超时
    allow_redirects = kwargs.get('allow_redirects')  # boolen 是否运行重定向
    proxies = kwargs.get('proxies')  # 代理
    verify = kwargs.get('verify')  # boolen 它控制我们是否验证服务器的TLS证书或字符串，在这种情况下，它必须是路径要使用的CA包。默认为“True”。
    stream = kwargs.get('stream')  # 如果``False``，则立即下载响应内容。
    cert = kwargs.get('cert')  # 如果是字符串，就是证书路径，如果是元组就是（证书，密钥）
    hooks = kwargs.get(
        'hooks')  # 信号事件处理  传递一个 {hook_name: callback_function} 字典给 hooks 请求参数若执行你的回调函数期间发生错误，系统会给出一个警告。若回调函数返回一个值，默认以该值替换传进来的数据。若函数未返回任何东西， 也没有什么其他的影响

    try:
        if verify == None or verify == "":
            verify = False

        r = requests.request(method=method, url=url, params=params, data=data, json=json, headers=headers,
                             cookies=cookies
                             , files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies
                             , verify=verify, stream=stream, cert=cert, hooks=hooks)
        return r
    except Exception as e:

        logging.info("请求错误: %s" % e+'\n')

#废弃
def jsonGetInfo(data, findData,dataName,findVaribleSep,nameVaribleSep):  # 在返回的json数据里查找对应数据,返回对应的值，str格式，data:接口返回的json数据或str数据，endData:查找的value的KEY值，相同的名称可以只填一个,未找到返回一个None，dataName:找到数据后存入的变量名
    #                                                 #数据和变量名按顺序配对
    try:
        resultList = []  # 查找结果数据
        if isinstance(data, str):
            pass
        else:
            data = str(data)
        data = data.strip()
        findData = findData.strip()
        dataName = dataName.strip()
        dataList = re.split('[^\s*\w_-]', data)
        dataList = list(filter(lambda x: x.strip() != '', dataList))
        findDataList = findData.split(findVaribleSep)
        dataNameList = dataName.split(nameVaribleSep)
        for i in dataList:
            for a in findDataList:
                if a == i:
                    index = [c for c, x in enumerate(dataList) if x == i]

                    for b in index:
                        result = dataList[b + 1]
                        resultList.append(a)
                        resultList.append(result)

        resultDict = {}
        endDict = {}
        for f in range(0, len(resultList), 2):
            resultDict[resultList[f]] = resultList[f + 1]
        if len(resultDict) != len(findDataList):
            noList = []
            for k in findDataList:
                if k not in resultDict:
                    noList.append(k)
            logging.info(str(noList) + '值未取到\n')
        for p in resultDict:
            Pindex = [c for c, x in enumerate(findDataList) if x == p]
            endDict[dataNameList[Pindex[0]]] = resultDict[p]
        return endDict

    except IndexError:
        logging.info('查找' + str(a) + '时，查找到的值为空，请检查输入是否正确！\n')
    except Exception as e:
        logging.info('jsonGetInfo:' + str(e)+'\n')

#废弃
def jsonGetFirstInfo(data, findData, dataName,findVaribleSep,nameVaribleSep):  # 在json数据内查找指定ID值，并保存第一个找到的值，如未找到则提示输入查找值不正确
    try:
        resultList = []  # 查找结果数据
        if isinstance(data, str):
            pass
        else:
            data = str(data)
        data = data.strip()
        findData = findData.strip()
        dataName = dataName.strip()
        dataList = re.split('[^\s*\w_-]', data)
        dataList = list(filter(lambda x: x.strip() != '', dataList))  # 拆解json成列表
        findDataList = findData.split(findVaribleSep)  # 查找值列表
        dataNameList = dataName.split(nameVaribleSep)  # 命名值列表
        for a in findDataList:
            for b in dataList:
                if a == b:
                    resultList.append(dataList[dataList.index(b) + 1])
                    break

        resultDict = {}
        if len(dataNameList) == len(resultList):

            for f in range(len(dataNameList)):
                resultDict[dataNameList[f]] = resultList[f]
            return resultDict
        else:
            logging.info('获取参数失败！请检查需要查找的数据与变量数是否一致!\n')
            raise ValueError

    except Exception as e:
        logging.info('jsonGetFirstInfo:' + str(e)+'\n')

#适用于json格式的变量替换
#废弃
def updateVaribleForDict(data,dict,separtor):      #从参数里确定变量位置和变量name，从变量字典内拿取数据填入
    try:
        for i in dict:
            if i == None:
                pass
            else:
                data = data.replace(separtor+i+separtor,'"'+str(dict[i])+'"')  #变量用配置文件的符号包裹

        return data
    except Exception as e:

        logging.info('查找变量名填入变量值:' + str(e)+'\n')


#适用于字符串的变量替换
def updateVaribleForStr(data,dict,separtor):      #从参数里确定变量位置和变量name，从变量字典内拿取数据填入
    try:

        for i in dict:
            if i == None:
                pass
            else:
              #变量用配置文件的符号包裹
                data = data.replace(separtor + i + separtor, str(dict[i]))
        return data
    except Exception as e:

        logging.info('查找变量名填入变量值:' + str(e)+'\n')


def sqlGetVarible(sql, varible,sqlSeq,varibleSep):  #查询sql获取结果，并将结果与变量名一一对应，返回一个字典，如数量不对应则返回一个None
    try:
        sqlList = sql.split(sqlSeq)
        mysql = con_Mysql()
        p = []
        for i in sqlList:
            mysql.sql = i
            logging.info('sql is {0}'.format(i)+'\n')

            r = mysql.select_sql()
            for a in r:
                for b in a:
                    if a[b] in p:
                        pass
                    else:
                        p.append(a[b])
            logging.info('sql results is {0}'.format(str(p))+'\n')

        mysql.end_con()
        varibleList = varible.split(varibleSep)
        varibleDict = {}
        if len(varibleList) == len(p):
            for l in range(len(p)):
                varibleDict[varibleList[l]] = p[l]

        else:
            # print('SQL返回的数据与设置的变量名数量不对应，请检查是否输入正确！')
            logging.info('SQL返回的数据与设置的变量名数量不对应，请检查是否输入正确！\n')
            varibleDict = None
        return varibleDict
    except Exception as e:
        logging.info('sql获取参数错误:'+str(e)+'\n')




def getImportInfo(r):  #传入请求响应，自动写入excel
    try:
        file =BASE_DIR+"/report/"+str(int(time.time()))+'.xlsx'
        f = open(file,'wb')
        f.write(r.content)
        f.close()
        return file
    except Exception as e:
        logging.info("获取导出数据错误 error is "+str(e)+'\n')



#输入预期结果时，对结果进行检测
def passTesting(jsonData,data,expectResultSep):
    try:
        dataList = str(data).split(expectResultSep)
        for i in dataList:
            if i in str(jsonData):
                pass
            else:
                return False
        return True
    except Exception as e:
        logging.debug('jsonData:'+str(jsonData) + ',data = ' + str(data)+'\n')
        logging.info("通过检测失败！"+str(e)+'\n')


#获取码文件的全部数据，处理成矩阵型数据
def mikCodeData(filePath):
    try:
        codingName = getFileCoding(filePath)
        with open(file=filePath,mode='r+',encoding=codingName) as f:
            dataLines = f.readlines()
            data = []
            for i in dataLines:
                l = i.split(',')
                data.append(l)
            f.close()
        return data
    except Exception as e:
        if f.closed:
            pass
        else:
            f.close()
        logging.info("获取文件数据失败："+str(e)+'\n')
#输入两位数序列号，获取数据
def getCodeInfo(codeData,row,colum):
    try:
        if isinstance(row,str) or isinstance(colum,str):
            row = int(row)
            colum = int(colum)

        data = codeData[row-1][colum-1]
        return data
    except Exception as e:
        logging.info("获取码数据失败："+str(e)+'\n')
#处理读取的excel标识数据，并切分处理成列表形式【str filePath，str index】
def cutCode(data,globalVariable):
    try:
        dList = data.split(':')
        result = [codePath+'/'+globalVariable[dList[0]],dList[1],dList[2]]
        return result
    except Exception as e:
        logging.info('输入的数据格式异常，不符合（fileA:2:3）格式或全局变量表内未找到文件变量名.\n')


fileInfo = {}

def updateCodeVarible(data,dict,separtor):
    try:
        global fileInfo
        dataList = data.split(separtor)

        if len(dataList) <=1:
            logging.info('查找变量名填入变量值-处理数据异常！\n')
            raise ValueError
        for i in range(1,len(dataList),2):
            endData = cutCode(data=dataList[i],globalVariable=dict)
            globeObj.CodeInfo.append(endData[0])
            globeObj.CodeInfo.append(endData[1])
            if endData[0] in fileInfo.keys():
                codeData = getCodeInfo(fileInfo[endData[0]], endData[1], endData[2])
            else:
                fileData = mikCodeData(endData[0])
                codeData = getCodeInfo(fileData,endData[1],endData[2])
                if fileData != None:
                    fileInfo[endData[0]] = fileData
            dataList[i] = codeData.replace('\n','')
        print(dataList)
        result = ''
        for b in dataList:
            result += b
        return result
    except Exception as e:
        logging.info('查找变量名填入变量值:' + str(e)+'\n')


def delFileData(file,index):
    try:
        index = list(index)
        index.sort()
        codingName = getFileCoding(file)
        data = open(file,'r+',encoding=codingName).readlines()
        with open(file, 'w+',encoding=codingName) as handle:
            k = 0
            for i in index:
                if isinstance(i, str):
                    i = int(i)

                data.remove(data[i-1-k])
                k+=1
            handle.writelines(data)
    except IndexError:
        logging.info('文件内数据不足，请检查！\n')

    except Exception as e:
        logging.info("删除数据失败："+str(e)+'\n')


#删除已使用过的码，整行删除
def delOldCodeData(data):
    try:
        oldList = []
        result = {}
        for i in range(0, len(data), 2):
            if data[i] in result:
                result[data[i]].add(int(data[i + 1]))
            else:
                result[data[i]] = {int(data[i + 1])}
        for k in result:
            delFileData(k,result[k])
            oldList.append('已删除文件'+k+'的第'+str(result[k])+'行数据')
        logging.info(str(oldList)+'\n')
    except Exception as e:
        logging.info("删除已使用过的码数据失败！:"+str(e)+'\n')


#遍历所有的值，查找需要寻找的值

def isInclude(data,Fdata):
    try:
        for i in data:
            if data[i] != Fdata[i]:
                return False
        return True
    except Exception as e:
        logging.info('数据异常！')
        return False
resultList = []
def JsonGetValue(data,finder,**kwargs):
    global resultList
    try:
        if isinstance(data,str):
            try:
                data = data.replace("'", '"')
                data = json.loads(data)
            except JSONDecodeError:
                logging.info("数据格式异常，非json格式。")
        if not isinstance(data,dict):
            logging.info("数据格式错误")
            raise KeyError
        jsonList_ext = []
        search = kwargs.get('search')
        if search != None:
            searchV = True
        else:
            searchV = False
        if isinstance(finder,str):
            finder = finder.split(',')
        data = [data]
        if resultList != []:
            data = data + resultList
        for i in data:
            if len(finder) == 1:
                result = {}
                if finder[0] in i.keys():
                    result[finder[0]] = i[finder[0]]
                    return (result,i)
                else:
                    for value in i.values():
                        if isinstance(value,dict):
                            jsonList_ext.append(value)
                        elif isinstance(value,list):
                            findDict(value)
            elif len(finder) >1:
                r = True
                result = {}
                for n in finder:

                    if n not in i.keys():
                        r = False
                        break
                    elif n in i.keys():
                        result[n]=i[n]

                if r and not searchV:

                    return (result,i)
                elif r and searchV:
                    isClude = isInclude(search, result)
                    if isClude:
                        return (result,i)
                    else:
                        for value in i.values():
                            if isinstance(value, dict):
                                jsonList_ext.append(value)
                            elif isinstance(value, list):
                                findDict(value)
                else:
                    for value in i.values():
                        if isinstance(value,dict):
                            jsonList_ext.append(value)
                        elif isinstance(value,list):
                            findDict(value)
        jsonList_ext = jsonList_ext + resultList
        resultList = []
        if len(jsonList_ext) != 0 :
            for p in jsonList_ext:
                if searchV:
                    result = JsonGetValue(p,finder,search=search)
                else:
                    result = JsonGetValue(p,finder)
                if result != None:
                    return result
        else:
            return None

    except Exception as e:
        logging.info("获取查找数据失败："+str(e))

def findDict(data):
    global resultList
    try:
        for i in data:
            if isinstance(i,dict):
                resultList.append(i)
            elif isinstance(i,list):
                findDict(i)
    except Exception as e:
        logging.info('查找字典失败！'+str(e))

def getVariableData(data):
    try:
        dataList = data.split(',')
        findList = []
        searchList = {}
        for i in dataList:
            if ":" in i:
                list_1 = i.split(':')
                findList.append(list_1[0])
                searchList[list_1[0]] = list_1[1]
            else:
                findList.append(i)
        return (findList,searchList)
    except Exception as e:
        logging.info("getVariableData 's error:" +str(e))

#压缩  解压 程 序
import os
import glob
import zipfile

def unzip_file(dir_path):
    # 解压缩后文件的存放路径
    unzip_file_path = r"\\ZIP"
    # 找到压缩文件夹
    dir_list = glob.glob(dir_path)
    if dir_list:
        # 循环zip文件夹
        for dir_zip in dir_list:
            # 以读的方式打开
            with zipfile.ZipFile(dir_zip, 'r') as f:
                for file in f.namelist():
                    f.extract(file, path=unzip_file_path)
            os.remove(dir_zip)

def zip_files(dir_path, zip_path,isDel=False):
    """
    :param dir_path: 需要压缩的文件目录
    :param zip_path: 压缩后的目录
    :return:
    """

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as f:
        for root, _, file_names in os.walk(dir_path):
            for filename in file_names:
                f.write(os.path.join(root, filename), filename)
                if isDel:
                    os.remove(os.path.join(root, filename))


def checkReport():
    try:
        reportPath = BASE_DIR + "/report"
        fileSize = 0
        for root, dirs, files in os.walk(reportPath, topdown=False):
            for file in files:
                fileSize += os.path.getsize(os.path.join(root, file))
        if fileSize >= 1024 * 1024 * 10:
            zip_files(reportPath, BASE_DIR + "/ZIP/" + str(int(time.time())) + '.zip', isDel=True)
    except Exception as e:
        logging.info("检测报告文件夹大小是否超过10MB失败："+str(e))