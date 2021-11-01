import socket
from threading import Thread
import time
import pickle

address = ('127.0.0.1', 11451)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

models: dict[str, list] = {}  # 模型列表
dataGroups: dict[str, tuple] = {}  # 数据列表


def registerModelServer(address, modelName):
    """
    注册一个模型服务器
    """
    if models.get(modelName) is None:
        models[modelName] = []
    models[modelName].append(address)


def registerDataServer(address, dataGroupName, count) -> bool:
    """
    注册一个数据集服务器，提供名称，数据集大小两种信息
    """
    if dataGroups.get(dataGroupName) is None:
        dataGroups[dataGroupName] = (address, count)
        return True
    else:
        return False


def getInfos():
    s1 = list(models.keys())
    s2 = [len(it) for it in models.values()]
    s3 = list(dataGroups.keys())
    s4 = [it[1] for it in dataGroups.values()]
    return pickle.dumps((s1, s2, s3, s4))


def requestProcess():
    while True:
        client, addr = server.accept()
        data = client.recv(8)
        try:
            if b'000' == data:
                # 模型服务器注册
                client.sendall(b'ok')
                data = client.recv(1024)
                addr, modelName = pickle.loads(data)
                registerModelServer(addr, modelName)
                client.sendall(b'ok')

            elif b'111' == data:
                # 模型服务器注销
                print('')
            elif b'222' == data:
                # 数据集服务器注册
                client.sendall(b'ok')
                data = client.recv(1024)
                addr, dataGroupName, count = pickle.loads(data)
                if registerDataServer(addr, dataGroupName, count):
                    client.sendall(b'ok')
                else:
                    client.sendall(b'fail')

            elif b'333' == data:
                # 数据集服务器注销
                print('')
            elif b'444' == data:
                # 请求模型、数据集信息
                data = getInfos()
                client.sendall(data)
            elif b'555' == data:
                # 请求模型服务器地址
                client.sendall(b'ok')
                data = client.recv(1024)
                key = pickle.loads(data)
                if models.get(key) is None:
                    client.sendall(b'fail')
                else:
                    ret = models[key][0]
                    data = pickle.dumps(ret)
                    client.sendall(data)
            elif b'666' == data:
                # 请求数据集服务器地址
                client.sendall(b'ok')
                data = client.recv(1024)
                key = pickle.loads(data)
                if dataGroups.get(key) is None:
                    client.sendall(b'fail')
                else:
                    ret = dataGroups[key][0]
                    data = pickle.dumps(ret)
                    client.sendall(data)
            else:
                client.sendall(b'fail')
        except BaseException:
            print(data)
            client.sendall(b'fail')

        client.close()


if '__main__' == __name__:
    thd = Thread(target=requestProcess)
    thd.daemon = True

    server.bind(address)
    server.listen(5)

    thd.start()
    while True:
        s = input()
        if 'stop' == s:
            server.close()
            break
        elif 'test' == s:
            print(models)
            print(dataGroups)
            print(getInfos())
        else:
            print('No such command')
            print('stop - stop server')
            print('test - output some test infomation')
