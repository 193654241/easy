import configparser
import re
import pymysql
import os
from tkinter import messagebox

global data
global cursor

def connectDB(serverIP,username,password):
    try:
        db = pymysql.connect(serverIP,username,password,"mysql" )
        # 使用 cursor() 方法创建一个游标对象 cursor
        global cursor
        cursor = db.cursor()
        return cursor
    except pymysql.err.OperationalError:
        messagebox.showinfo('提示','数据库参数错误')
def createPojo(database,oldpath,newpath,name,package): #创建Pojo
    oldfile = open(os.path.join(oldpath,"Pojo.java"),'r',encoding='utf8')
    newfile = open(os.path.join(newpath,name.capitalize()+'.java'),'w',encoding='utf8')
    of = oldfile.read()
    field = ('\t${id}\n'
        '\tprivate ${type} ${column};\n')
    getset = (	'\tpublic ${type} get${Column}() {	\n'	
		'\t\treturn ${column};\n'
	'\t}\n'
	'\tpublic void set${Column}(${type} ${column}) {\n'
	'\t\tthis.${column} = ${column};\n'
	'\t}\n\n')
    
    try:
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute("show columns from "+name+" from "+database)
        # 使用 fetchall() 方法获取全部数据.
        global data
        fields = ''
        getsets = ''
        data = cursor.fetchall()
        for database in data:
            lenth = len(database)
            for i in range(lenth):
                if i==0:
                    f = replace(field,{'${column}':database[0],'${Column}':database[0].capitalize()})
                    g = getset
                if i==1:
                    if database[1].find('int')>-1:
                        f = replace(f,{'${type}':'Integer','${column}':database[0]})
                        g = replace(g,{'${type}':'Integer','${column}':database[0],'${Column}':database[0].capitalize()})
                    if database[1].find('varchar')>-1:
                        f = replace(f,{'${type}':'String','${column}':database[0]})
                        g = replace(g,{'${type}':'String','${column}':database[0],'${Column}':database[0].capitalize()})
                    if database[1].find('year')>-1:
                        f = replace(f,{'${type}':'String','${column}':database[0]})
                        g = replace(g,{'${type}':'String','${column}':database[0],'${Column}':database[0].capitalize()})
                if i==3:
                    if database[3].find('PRI')>-1:
                        f = replace(f,{'${id}':'@Id'})
                    else:
                        f = replace(f,{'${id}':''})
            fields = fields + f 
            getsets = getsets + g
        of = replace(of,{'${columns}':fields,'${getsets}':getsets,'${package}':package,'${name}':name,'${cname}':name.capitalize()})
        newfile.write(of+'\n')
    except KeyError:
        print('key not found')
def createDao(oldpath,newpath,name,package): #创建Dao
    oldfile = open(os.path.join(oldpath,"Dao.java"),'r',encoding='utf8')
    newfile = open(os.path.join(newpath,name.capitalize()+"Dao.java"),'w',encoding='utf8')
    of = replace(oldfile.read(),{'${cname}':name.capitalize(),'${name}':name,'${package}':package})
    newfile.write(of)
def createService(oldpath,newpath,name,package): #创建Service
    oldfile = open(os.path.join(oldpath,"Service.java"),'r',encoding='utf8')
    newfile = open(os.path.join(newpath,name.capitalize()+"Service.java"),'w+',encoding='utf8')
    global data
    condition = ( '\t\t\t\t// ${column}\n'
        ' \t\t\t\tif (searchMap.get("${column}")!=null && !"".equals(searchMap.get("${column}"))) {\n'
        '\t\t\t\t\tpredicateList.add(cb.like(root.get("${column}").as(String.class), "%"+(String)searchMap.get("${column}")+"%"));\n'
        '\t\t\t\t}\n\n')
    conditions = ''
    for database in data:
        for i in range(len(database)):
            if i==0:
                c = replace(condition,{'${column}':database[i]})
        conditions = conditions + c
    of = replace(oldfile.read(),{'${封装条件}':conditions,'${cname}':name.capitalize(),'${name}':name,'${package}':package})
    newfile.write(of)
def createController(oldpath,newpath,name,package): #创建Controller
    oldfile = open(os.path.join(oldpath,"Controller.java"),'r',encoding='utf8')
    newfile = open(os.path.join(newpath,name.capitalize()+"Controller.java"),'w+',encoding='utf8')
    of = replace(oldfile.read(),{'${package}':package,'${name}':name,'${cname}':name.capitalize()})
    newfile.write(of)
def replace(s,map):
    for m in map:
        s = s.replace(m,map[m])
    return s

##connectDB()
##createPojo('test','default_template\src\main\java\com\pojo','temp','book','com.project')
##createDao('default_template\src\main\java\com\dao','temp','book','com.project')
##createService('default_template\src\main\java\com\service','temp','book','com.project')
##createController('default_template\src\main\java\com\controller','temp','book','com.project')
##map = {'${a}':'c','${b}':'d'}
##replace('${a}${a}${a}${c}${b}',{'${a}':'c'})
