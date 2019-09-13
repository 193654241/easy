#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *               # 导入 Tkinter 库
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askdirectory

import configparser

import time
import pymysql
import os

import create #三层架构等文件创建

global cursor
config = configparser.ConfigParser()


def addini():
    config.read('default.ini')
    serverIP.set(config['DEFAULT']['ip'])
    username.set( config['DEFAULT']['username'])
    password.set( config['DEFAULT']['password'])
    templatePath.set(config['DEFAULT']['templatePath'])
    codePath.set(config['DEFAULT']['codePath'])
def inifile():
    os.system('start explorer default.ini')
def key(event):
    packName.set('com.'+projectName.get())
def event(event):
    print("event")
    try:
        toSettingTemplateWindow()
    except BaseException:
        messagebox.showerror('提示','连接错误')

def callback():
    print("回调函数")
def goBack():
    settingTemplateWindow.withdraw()
    root.deiconify()#两步显示窗口
def openDirectory():
    templatePath.set(askdirectory())
    print(templatePath.get())
def openFile():
    codePath.set(askdirectory())
    print(codePath.get())
def mkdir(path):
    # 去除首位空格
    #path=path.strip()
    # 去除尾部 \ 符号
    #path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        #print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print (path+' 目录已存在')
        return False
def createCode():
    if projectName.get()=='':
        messagebox.showinfo('提示','项目名不能为空')
        return
    t = templatePath.get()
    p = codePath.get()
    lenth = len(t)
    for root,dirs,files in os.walk(t):
        for dir in dirs:
            #print(p,root,dir,root[lenth:])
            #获取目录的名称
            #print(dir)
            #获取目录的路径
            #print(os.path.join(root,dir))
            # 定义要创建的目录
            mkpath = os.path.join(p+"/"+projectName.get()+root[lenth:],dir)
            # 调用函数
            #print(root)
            if dir == 'common':
                mkdir(mkpath)
            else:
                mkdir(mkpath.replace('com','com/'+projectName.get()))
        for file in files:
            #获取文件所属目录
            #print(root)
            #获取文件路径
            filepath = os.path.join(root,file)
            #print(root)
            newfilepath = (p+"/"+projectName.get()+"/"+root[lenth:]).replace('com','com/'+projectName.get())
            staticfile = (file.split('.',1))[1]
            if staticfile == 'java':
                print(file)
                if file=='Pojo.java':
                    if tableList.get()!='全部表':
                        create.createPojo(libraryList.get(),root,newfilepath,tableList.get(),packName.get())
                        continue
                    else:
                        for t in tableList['value']:
                            if t[0]!='全':
                                create.createPojo(libraryList.get(),root,newfilepath,t[0],packName.get())
                        continue
                if file=='Dao.java':
                    if tableList.get()!='全部表':
                        create.createDao(root,newfilepath,tableList.get(),packName.get())
                        continue
                    else:
                        for t in tableList['value']:
                            if t[0]!='全':
                                create.createDao(root,newfilepath,t[0],packName.get())
                        continue
                if file=='Service.java':
                    if tableList.get()!='全部表':
                        create.createService(root,newfilepath,tableList.get(),packName.get())
                        continue
                    else:
                        for t in tableList['value']:
                            if t[0]!='全':
                                create.createService(root,newfilepath,t[0],packName.get())
                        continue
                if file=='Controller.java':
                    if tableList.get()!='全部表':
                        create.createController(root,newfilepath,tableList.get(),packName.get())
                        continue
                    else:
                        for t in tableList['value']:
                            if t[0]!='全':
                                create.createController(root,newfilepath,t[0],packName.get())
                        continue
                f=open(p+"/"+projectName.get()+filepath[lenth:].replace('com','com/'+projectName.get()), 'w+',encoding='utf8')
                config.read('default.ini')
                of = open(filepath,encoding='utf8')
                txt = of.read()
                for item in config.items('代码生成配置'):
                    txt = txt.replace('${'+item[0]+'}',item[1])
                txt = create.replace(txt,{'${package}':packName.get()})
                f.write(txt)
            elif(staticfile == 'xml'  or staticfile=='yml'or staticfile=='txt'or staticfile=='css'or staticfile=='html'or staticfile=='ftl'):
                f=open(p+"/"+projectName.get()+filepath[lenth:],'w',encoding='utf8')
                config.read('default.ini')
                of = open(filepath,encoding='utf8')
                txt = of.read()
                for item in config.items('代码生成配置'):
                    txt = txt.replace('${'+item[0]+'}',item[1])
                txt = create.replace(txt,{'${package}':packName.get(),'${port}':'80','${application}':projectName.get()})
                f.write(txt)
            else:
                f=open(p+"/"+projectName.get()+filepath[lenth:],'ab+')
                f.write(open(filepath,'rb').read())
def destroy():
    root.destroy()
def helpwindow():
    helpWindow=Toplevel(root,width=350,height=500)
    helpWindow.resizable(0,0)
    helpWindow.title('说明文档-1.0')
    Label(helpWindow, text='1.输入数据库帐号密码连接并选择数据库\n\n'+
          '2.点击下一步\n\n'+
          '3.选择模板\n\n'+
          '4.选择自定义的文档结构路径\n\n'+
          '5.输入其它数据，点击生成代码\n'+
          '\n\n\n\n  ---编程爱好者,开发合作---\nQQ193654241\nQ群866536299'
          ).place(x=150,y=200,anchor=CENTER)
    
    # print(template.current())
    # askdirectory()                          #文件夹对话框
    # filename=filedialog.askopenfilename()  #文件对话框
    # print(len(libraryList['value']))
    # root.withdraw()#隐藏窗口
    # time.sleep(5)
    # root.update()
    # root.deiconify()#两步显示窗口


def libraryListHandle(*args):   #处理事件，*args表示可变参数
    cursor.execute("use "+libraryList.get())
    cursor.execute('show tables')
    data = cursor.fetchall()
    tableList['value']= ('全部表',) + data
    for database in data:
        print ("Table : %s " % database)
    print(tableList.get()) #打印选中的值
    tableList.current(0)

def tableListHandle(*args):   #处理事件，*args表示可变参数
    #print(tableList.get()) #打印选中的值

    for t in tableList['value']:
        print(t[0])
    

def toSettingTemplateWindow():
    if connectDB()=='true':
        root.withdraw()#隐藏窗口
        #settingTemplateWindow=Toplevel(root,width=570,height=500)
        settingTemplateWindow.title('代码生成器 --yuren')
        settingTemplateWindow.resizable(0,0)
        settingTemplateWindow.deiconify()

        author.set("渔人")
        libraryListHandle(tableList.get())
        
def connectDB(): #测试连接数据库
    try:
        global cursor
        cursor = create.connectDB(serverIP.get(),username.get(),password.get())
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute("show databases")
        # 使用 fetchall() 方法获取全部数据.
        data = cursor.fetchall()
        for database in data:
            print ("Database : %s " %database)
        libraryList['value']=data
        libraryList.current(0)
        # 关闭数据库连接
        #db.close()
        return 'true'
    except pymysql.err.OperationalError:
        messagebox.showinfo('提示','数据库参数错误')
        

root=Tk()                           # 创建窗口对象
root.geometry("+600+350")           # 设置窗口位置
root.title("代码生成器 --yuren") # 配置窗口标题
root.geometry("500x300")           # 配置窗口大小
root.resizable(0,0)                 # 禁止调整窗口大小
root.bind("<Return>",event)

canvas = tk.Canvas(root, width=500,height=300,bd=0, highlightthickness=0)
photo = PhotoImage(file='3.png')
canvas.create_image(200, 250, image=photo)
canvas.place(x=0,y=0)

settingTemplateWindow=Toplevel(root,width=570,height=500)
settingTemplateWindow.withdraw()

DBTypeList = ttk.Combobox(root)
DBTypeList['value'] = ('mysql','oracle')
DBTypeList['state'] = ('readonly')
DBTypeList.current(0)  #选择第一个
#DBTypeList.bind("<<ComboboxSelected>>",go)  #绑定事件,(下拉列表框被选中时，绑定go()函数)
DBTypeList.place(x=200,y=30)

Label(root,text="请选择数据库类型:").place(x=200,y=30,anchor=NE)    #靠右,左是W
Label(root,text="服务器IP:").place(x=200,y=85,anchor=NE)    #靠右,左是W
Label(root,text="用户:").place(x=200,y=120,anchor=NE)    #靠右,左是W
Label(root,text="密码:").place(x=200,y=155,anchor=NE)    #右是E


serverIP = StringVar()
username = StringVar()
password = StringVar()
serverIP_=Entry(root, textvariable=serverIP,highlightcolor='red', highlightthickness=1,fg='green').place(x=200,y=85)              #输入框
username_=Entry(root, textvariable=username,highlightcolor='red', highlightthickness=1,fg='green').place(x=200,y=120)             #输入框
password_=Entry(root, textvariable=password,highlightcolor='red', highlightthickness=1,fg='green',show="*").place(x=200,y=155)    #输入框


Button(root,text="下一步",bg="LightBlue",command=toSettingTemplateWindow).place(x=330,y=220)

Button(root,text="配置",bg="LightBlue",command=inifile).place(x=400,y=270)
Button(root,text="使用说明",bg="LightBlue",command=helpwindow).place(x=440,y=270)


#template = ttk.Combobox(settingTemplateWindow)
#template['value'] = ('--请选择模板--','spring2.x全家桶','springcloud')
#template['state'] = 'readonly'
#template.current(0)  #选择第一个
##template.bind("<<ComboboxSelected>>",go)  #绑定事件,(下拉列表框被选中时，绑定go()函数)
#template.place(x=220,y=25)
Canvas(settingTemplateWindow,bg='gray',height=2,width=570).place(x=0,y=55)# 分隔线1


templatePath = StringVar()
codePath = StringVar()
projectName = StringVar()
packName = StringVar()
projectChineseName = StringVar()
author = StringVar()

Button(settingTemplateWindow,text="返回上一步",bg="#FF3030",command=goBack).place(x=40,y=15)
Label(settingTemplateWindow,text="结构文档路径").place(x=150,y=80)
templatePath_=Entry(settingTemplateWindow, textvariable=templatePath).place(x=240,y=80)
Button(settingTemplateWindow,text="选择",command=openDirectory).place(x=400,y=80)
Label(settingTemplateWindow,text="代码生成路径").place(x=150,y=120)
codePath_=Entry(settingTemplateWindow, textvariable=codePath).place(x=240,y=120)
Button(settingTemplateWindow,text="选择",command=openFile).place(x=400,y=120)
Canvas(settingTemplateWindow,bg='gray',height=2,width=570).place(x=0,y=150)# 分隔线2
Label(settingTemplateWindow,text="项目名(英文)").place(x=150,y=160)
projectName_=Entry(settingTemplateWindow, textvariable=projectName).place(x=240,y=160)
settingTemplateWindow.bind("<Key>", key)
Label(settingTemplateWindow,text="包名").place(x=150,y=200)
packName_=Entry(settingTemplateWindow, textvariable=packName).place(x=240,y=200)
##Label(settingTemplateWindow,text="项目中文名称").place(x=150,y=240)
##projectChineseName_=Entry(settingTemplateWindow, textvariable=projectChineseName).place(x=240,y=240)
Label(settingTemplateWindow,text="作者").place(x=150,y=280)
author_=Entry(settingTemplateWindow, textvariable=author).place(x=240,y=280)
Label(settingTemplateWindow,text="数据库").place(x=150,y=320)

libraryList = ttk.Combobox(settingTemplateWindow)
libraryList['value'] = ('--请先连接数据库--')
libraryList['state'] = 'readonly'
libraryList.current(0)  #选择第一个
libraryList.bind("<<ComboboxSelected>>",libraryListHandle)  #绑定事件,(下拉列表框被选中时，绑定go()函数)
libraryList.place(x=240,y=320)
#Button(root,text="连接数据库",bg="LightBlue",command=connectDB).place(x=100,y=220)

tableList = ttk.Combobox(settingTemplateWindow)
tableList['value'] = ('--请选择表--','all')
tableList['state'] = 'readonly'
tableList.current(0)  #选择第一个
tableList.bind("<<ComboboxSelected>>",tableListHandle)  #绑定事件,(下拉列表框被选中时，绑定go()函数)
tableList.place(x=240,y=360)


#Label(settingTemplateWindow,text="用户名").place(x=150,y=360)
#username_=Entry(settingTemplateWindow, textvariable=username).place(x=240,y=360)
#Label(settingTemplateWindow,text="密码").place(x=150,y=400)
#password_=Entry(settingTemplateWindow, textvariable=password).place(x=240,y=400)
Button(settingTemplateWindow,text="生成代码",bg="LightBlue",command=createCode).place(x=100,y=440)
Button(settingTemplateWindow,text="关闭程序",bg="LightBlue",command=destroy).place(x=400,y=440)





# 配置窗口风格
style = ttk.Style()
style.map('TCombobox',
          foreground=[('pressed', 'red'), ('active', 'red')],
          background=[('pressed', '!disabled', 'black'), ('active', 'white')],
          selectground=[("readonly","red")]
          )
#判断配置文件是否存在，存在就加载数据，不存在就新建文件再加载数据
if os.path.exists('default.ini'):
    addini()
else:
    config.read('default.ini')
    config['代码生成配置'] = {'举个栗子':'test'}
    config['DEFAULT'] = {'ip': '127.0.0.1',
                         'username': 'root',
                         'password': 'root',
                         'templatePath ':'templatePath ',
                         'codePath':'codePath'}
    with open('default.ini', 'w') as configfile:
        config.write(configfile)
root.mainloop()


