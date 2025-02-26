from microbit import *
#*****************************WIFI模块内部代码***************************************************
class Obloq(object):
    def connectWifi(self,SSID,PASSWORD,TIME):
        uart.write('AT+CWJAP="%s","%s"\r\n' %(SSID, PASSWORD))      # 设置wifi模块连接无线网络
        display.scroll("wait...");display.show(Image.HAPPY)
        uart.write('AT+CIPMUX=0\r\n');sleep(500)                   # 设置WIFI模块单路链接模式
        uart.write('AT+CIPSTART="TCP","0",0\r\n');sleep(TIME)   
        if uart.any():                                              #第二次读，返回服务器IP设置消息
            data = str(uart.readall(), "UTF-8");sleep(100)    
        uart.write('AT+CIFSR\r\n');sleep(200);data=0               # 设置这个后 读串口返回绑定ip 
        if uart.any():
            data = str(uart.readall(), "UTF-8")
            temp = data.split("\"",5)
            self.ip_address = temp[1]
            if self.ip_address[0]=='1' and len(self.ip_address)>10: 
                return True
            else:
                display.show(".");sleep(300)
                return False     
        else:
            display.show(".");sleep(300)
            return False
    def ifconfig(self):
        return self.ip_address
    def httpSet(self,IP,PORT):
        uart.write('AT+CIPSTART="TCP","%s",%s\r\n' %(IP, PORT))  
        sleep(6000)
        uart.write('AT+CIPMODE=1\r\n')  # 设置WIFI模块为透穿模式
        sleep(500)
        uart.write('AT+CIPSEND\r\n')  # 在透穿模式下开始发送数据
        sleep(2000)
        if uart.any():  # 如果串口有值
            self.res = str(uart.readall(), "UTF-8")
            self.res = 0
    def get(self,url,time):
        uart.write('GET /'+ url + '\r\n\r\n')  
        sleep(1000)
        if uart.any():  # 如果串口有值
            res = str(uart.readall(), "UTF-8")  
            return (200,res)
        return (404,"NOT FOUND")
Obloq = Obloq()
#***********************************************************************************************
# 串口初始化
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin12, rx=pin8)    
IP="172.16.204.56"
PORT="8000"
SSID="604"      ####这个东西
PASSWORD="xjzx@604"       ####这个东西

while Obloq.connectWifi(SSID,PASSWORD,10000) != True:
    display.show(".")
Obloq.httpSet(IP,PORT)
import Servo 
sv=Servo(pin0)
while True:
    val1=pin1.read_analog()
    errno,resp=Obloq.get("timecal?id=1&val1="+str(val1),10000)
    if errno==200:
        if resp=='on':
            sv.angle(0)
            sleep(1000)
            sv.angle(90)
            sleep(1000)
            sv.angle(180)
            sleep(1000)
            sv.angle(90)
            sleep(1000)
            display.show(Image.ANGRY)            
        else:
            display.show(Image.SAD)
    else: display.show(str(errno))
    sleep(1000)