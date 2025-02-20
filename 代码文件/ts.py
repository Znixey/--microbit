import sqlite3
from datetime import datetime as abc
from flask_wtf import *
from flask_bootstrap import *
from flask import *
from wtforms import *
import serial
cat=Flask(__name__)
cat.config['SECRET_KEY'] = '123456'
bootstrap=Bootstrap(cat)
#登录
class sb1(FlaskForm):
    usn=StringField("用户名")
    psw=StringField("密码")
    s1=SubmitField('注册')
class sb2(FlaskForm):
    usn=StringField("用户名")
    psw=StringField("密码")
    s2=SubmitField("登录")  
@cat.route("/loes",methods=["GET","POST"])
def res():
    sb3=sb1()
    sb4=sb2()
    if sb3.validate_on_submit():
        if sb3.s1.data:
            un=sb3.usn.data
            pw=sb3.psw.data
            d=seek(un,pw)
            if d==False:
                add(un,pw)
                return redirect('/checkok')
    if sb4.validate_on_submit():
        if sb4.s2.data:
            un=sb4.usn.data
            pw=sb4.psw.data
            d=seek(un,pw)
            if d=='1':
                return redirect('/enjoy1')
            else: print(d)
    return render_template('滑动.html',sb1=sb3,sb2=sb4)
class ok(FlaskForm):
    s1=SubmitField('进入页面')
@cat.route('/checkok',methods=["GET","POST"])
def oks():
    r=ok()
    if r.validate_on_submit():
        if r.s1.data:
            return redirect('/enjoy1')
    return render_template('ok.html',rr=r)
#用户信息查找
def seek(un,pw):
    conn=sqlite3.connect('user.db')
    cu=conn.cursor()
    sql="select * from data_u where username=?"
    cu.execute(sql,[un])
    h=cu.fetchall()
    print(h)
    print(un)
    if len(h)!=0:
        if h[0][1]==pw:
            return '1'
    else: return len(h)!=0
@cat.route('/video',methods=["GET","POST"])
def video():
    return render_template('video.html')
#注册信息
def add(un,pw):
    conn=sqlite3.connect('user.db')
    cu=conn.cursor()
    sql="insert into data_u(username,password) values(?,?)"
    cu.execute(sql,(un,pw))
    conn.commit()


#主页
class fh(FlaskForm):
    eat=SubmitField("进行投喂") 
    photo=SubmitField('拍照') 
@cat.route("/enjoy1",methods=["GET","POST"])
def enjoy():
    global zt1
    zt1=1
    key=fh()
    if key.validate_on_submit():
        if key.eat.data:
            print(1)
        if key.photo.data:
            return redirect('/video')
    pu=sqlite3.connect("pu.db")
    woo=pu.cursor()
    woo.execute("select * from puputime")
    pu.commit()
    data=woo.fetchall()
    h=[]
    for i in range(len(data)):
        h.append([])
        for j in range(1,4):
            h[i].append(data[i][j])
    woo.close()
    pu.close()
    sb=ask()
    return render_template('enj.html',data1=h,here=sb,fh1=key)
#状态查找
def ask():
    zt=sqlite3.connect("dqzt.db")
    ztr=zt.cursor()
    ztr.execute("select hw1 from sensorlog order by id desc limit 0,1;") #红外传感器的记录，需要一行初始状态（0），hw1是猫砂盆对应的红外传感器
    hw=ztr.fetchall()
    hw=hw[0][0]
    print('hw:',hw)
    if hw==1: 
        inls=timecheck()
        return '进入猫砂盆,已持续时间：'+str(inls)
    else: return '不在捏' 
#持续时间计算
def timecheck():
    global ans
    start=ans[0]
    start=start.strip()
    start=abc.strptime(start,'%Y-%m-%d %H:%M:%S')  
    nowt=abc.now()
    nowt=nowt.strftime('%Y-%m-%d %H:%M:%S')
    nowt=nowt.strip() 
    nowt=abc.strptime(nowt,'%Y-%m-%d %H:%M:%S') 
    last=(nowt-start).seconds
    return last
ans=[]
zt1=0
#时间计算
class wuwu(FlaskForm):
    yes=SubmitField("拉") 
    no=SubmitField('不拉') 
@cat.route("/timecalc",methods=["GET","POST"])
def timecal():
    wowo=wuwu()
    global ans,zt1
    if wowo.validate_on_submit():
        if wowo.yes.data:
            zt1=1
            print(1)
        if wowo.no.data:
            zt1=0
    zt=sqlite3.connect('dqzt.db')
    ztr=zt.cursor()
    ztr.execute('select * from sensorlog order by id desc limit 0,1;')
    zt.commit()
    hey=ztr.fetchall()
    past=hey[0][1]  
    now=zt1
    nowt=abc.now()      
    nowt=nowt.strftime('%Y-%m-%d %H:%M:%S')       
    print('past:',past,'now:',now)
    qu=sqlite3.connect('pu.db')
    woo=qu.cursor()
    print(nowt)
    if past!=now:
        print('enter')
        sql="insert into sensorlog(hw1) values("+str(zt1)+")"
        ztr.execute(sql)
        zt.commit()
        if past==1:
            print('ans=',ans)
            ans.append(nowt)
            ans[0]=ans[0].strip()
            ans[1]=ans[1].strip()
            att=abc.strptime(ans[0],'%Y-%m-%d %H:%M:%S')  ##
            btt=abc.strptime(ans[1],'%Y-%m-%d %H:%M:%S')  ##
            last=(btt-att).seconds
            ans.append(last)
            woo.execute('insert into puputime(start,end,long) values(?,?,?)',(ans[0],ans[1],ans[2]))
            qu.commit()
            print('insert ok!')
        else:
            ans=[nowt]
            print('update ok!')
    print('ans:',ans)
    woo.close()
    qu.close()
    ztr.close()
    zt.close()
    return render_template('6.html',fh1=wowo)
cat.run('127.0.0.1',port=8000,debug=True)