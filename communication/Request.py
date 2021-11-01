import socket
import pickle
from .CheckResult import CheckResultPresentation as Result
import client as cli


def getBaseInfo(ip: str):
    """
    获取基本信息，连接失败时候返回None
    否则返回包含服务器信息的四元组
    """
    address = (ip, 11451)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(address)
        client.sendall(b'444')
        data = client.recv(1024)
        info = pickle.loads(data)
        client.close()
        return info
    except BaseException:
        client.close()
        return None


def getServerInfo(ip: str, modelName: str, dataGroupName: str):
    """
    获取模型信息及数据库信息
    """
    address = (ip, 11451)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(address)
        client.sendall(b'555')
        data = client.recv(8)
        if b'ok' == data:
            key = pickle.dumps(modelName)
            client.sendall(key)
            data = client.recv(1024)
            modelAddr = pickle.loads(data)
        else:
            client.close()
            return None

        client.sendall(b'666')
        data = client.recv(8)
        if b'ok' == data:
            key = pickle.dumps(dataGroupName)
            client.sendall(key)
            data = client.recv(1024)
            dataAddr = pickle.loads(data)
        else:
            client.close()
            return None

        client.close()
        return (modelAddr, dataAddr)
    except BaseException:
        client.close()
        return None


def duplicateResultGet(address: str, lines: list) -> list:
    """
    收发查重包
    """
    # TODO: 测试
    import time
    time.sleep(1)

    tar = list(range(1, 17))
    raw = cli.duplicateCheck(lines, tar, 0.7, 3)
    parsed = cli.parse(raw, lines)
    response = []
    for i in parsed.values():
        response.append(Result(*i))
    return response

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(address)
        data = pickle.dumps(lines)
        client.sendall(data)
        data = client.recv(65536)
        ret = pickle.loads(data)
        client.close()
        return [Result(it[0], it[1], it[2]) for it in ret]
    except BaseException:
        client.close()
        return None
