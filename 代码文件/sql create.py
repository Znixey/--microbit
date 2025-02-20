#用于初始化数据库（将相应db删掉后在这里创建即可
import sqlite3
n=int(input())
while n!=0:
    if n==1:
        conn=sqlite3.connect('user.db')
        cu=conn.cursor()
        sql='create table data_u(username varchar(50),password text)'
        cu.execute(sql)
        conn.commit()
        print('ok!')
    elif n==2:
        pu=sqlite3.connect('pu.db')
        woo=pu.cursor()
        sql='create table puputime("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,start datetime,end datetime,long datetime)'
        woo.execute(sql)
        pu.commit()
        print('ok!')
    elif n==3: 
        zt=sqlite3.connect("dqzt.db")
        ztr=zt.cursor()
        sql='create table sensorlog("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,hw1 int)'
        ztr.execute(sql)
        zt.commit()
        print('ok!')
        sql='insert into sensorlog(hw1) values(0)'
        ztr.execute(sql)
        zt.commit()
        print('insert ok!')
    n=int(input())
print('over')