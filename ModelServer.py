import pickle
import socket
import sys
from threading import Thread

address = ('127.0.0.1', 11452)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
modelName = "测试模型"


def requestProcess():
    while True:
        client, addr = server.accept()
        data = client.recv(8)


if '__main__' == __name__:
    addr = ('127.0.0.1', 11451)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    client.sendall(b'000')
    data = client.recv(16)
    if b'ok' == data:
        data = pickle.dumps((address, modelName))
        client.sendall(data)
        data = client.recv(16)

    client.close()
    if b'ok' != data:
        print("模型注册状态：" + str(data))
        sys.exit()

    thd = Thread(target=requestProcess)

    server.bind(address)
    server.listen(5)
    thd.start()
    while True:
        s = input()
        if 'stop' == s:
            server.close()
            #TODO: 注销模型服务器
            break
        else:
            print('No such command')
            print('stop - stop server')
