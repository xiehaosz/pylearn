#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket

def run_server():
    # 创建一个socket对象，默认TCP套接字
    s = socket.socket()
    # 绑定端口
    s.bind(('127.0.0.1', 9006))
    # 监听端口
    s.listen(5)
    print("正在连接中……")

    # 建立连接之后，持续等待连接
    while 1:
        # 阻塞等待连接
        sock, addr = s.accept()
        print(sock, addr)
        # 一直保持发送和接收数据的状态
        while 1:
            text = sock.recv(1024)
            # 客户端发送的数据为空的无效数据
            if len(text.strip()) == 0:
                print("服务端接收到客户端的数据为空")
            else:
                print("收到客户端发送的数据为：{}".format(text.decode()))
                content = input("请输入发送给客户端的信息：")
                # 返回服务端发送的信息
                sock.send(content.encode())
        sock.close()


def run_client():
    my_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_client.connect(("70.56.69.97", 9006))
    my_client.send(("%s\n" % 'this is a message').encode("utf-8"))

    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)   # 获取自己的主机ip
    print(host, host_ip)

    # _res = sys._getframe()
    # if hasattr(_res, "f_back"):                 # 调用者文件名
    #     fname = _res.f_back.f_code.co_filename
    #     if hasattr(_res, "f_code"):             # 调用者函数名
    #         funcname = _res.f_back.f_code.co_name
    #         lineno = _res.f_back.f_lineno       # 调用者所在行号
