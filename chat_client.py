"""
 搭建数据报套接字 客户端
"""
from socket import *
import os,sys
#服务器地址
ADDR=('172.40.71.183',8890)
# 发送消息
def send_msg(s,name):
    while True:
        try:              # ctrl + c 退出
            text = input("发言：")
        except KeyboardInterrupt:
            text='quit'

        if text=='quit':       #退出聊天室
            msg="Q " + name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)
# 接收消息
def recv_msg(s):
    while True:
        data,addr=s.recvfrom(2048)
        if data.decode() == 'EXIT':  #服务端返回信息 让接收消息进程退出
            sys.exit()
        print(data.decode() + "\n发言：",end='')  #防止覆盖 加个发言
#创建网络连接
def main():
    s=socket(AF_INET,SOCK_DGRAM)   # 在父进程中创建套接字
    while True:
        name =input("请输入姓名：")
        msg="L "+name
        s.sendto(msg.encode(),ADDR)
        # 等待回应
        data,addr=s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    # 进入聊天室后创建新进程
    pid = os.fork()
    if pid<0:
        sys.exit("Error!")
    elif pid ==0:
        send_msg(s,name)  #子进程从父进程内存空间获取套接字，那么父子进程对该对象的操作会有一定的属性关联
    else:
        recv_msg(s)
if __name__=="__main__":
    main()






