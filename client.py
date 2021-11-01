import os
import re
import numpy as np
from sentence_transformers import SentenceTransformer
import sklearn.preprocessing as prepro
import config
import pickle
from time import time

start = time()
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
# model = model.cuda()
print("model load time:", time() - start)
start = time()
if os.path.exists(config.databasePath):
    with open(config.databasePath, "rb") as f:
        database = pickle.load(f)
print("database load time:", time() - start)


def splitPara(para, thres=20):
    ori = para
    para = re.sub('\n', ' ', para)
    para = re.sub("([，。！？；])([^：])", r"\1\n\2", para)
    para = re.sub('(\.{6})([^：])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^：])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([：:][“‘])([^：:])', r'\1\n\2', para)
    para = re.sub('[“‘”’]', ' ', para)
    para = re.sub('[　—]', ' ', para)  # 删除中文的宽空格、连字符
    para = re.sub('\n+', '\n', para)  # 删除多余的换行符
    para = para.rstrip()  # 删除段尾的换行符
    texts = para.split("\n")

    idx = 0
    while idx < len(texts):
        if len(texts[idx]) < thres and idx != len(texts) - 1:
            texts[idx] = texts[idx] + texts[idx + 1]
            del texts[idx + 1]
        else:
            idx += 1

    nowpos = 0
    pos_list = []
    for i in range(0, len(texts)):
        (begin, end) = (nowpos, nowpos + len(texts[i]))
        nowpos = end
        pos_list.append((begin, end))

    return texts, pos_list


def sent2vec(sent):
    vec = model.encode(sent)
    vec = prepro.normalize(vec.reshape(1, -1))
    return vec


def lines2data(lines):
    pos = []
    text = []
    vec = []

    for i in range(len(lines)):
        line = lines[i].strip()
        if len(line) > 0:
            sents, onePos = splitPara(line)
            for j in range(len(sents)):
                text.append(sents[j])
                vec.append(sent2vec(sents[j]))
                pos.append((i, *onePos[j]))

    vec = np.vstack(vec)
    return pos, text, vec


def duplicateCheck(lines, tars, thres, k):
    """
    :param lines: 列表，每一个元素是查询文章的一行，或者说一段，即只有一个回车
    :param tars: 指定数据库中文章序号
    :param thres: 相似度阈值
    :param k: 一句话最多返回k个重复
    :return:
    列表，每一个元素为(docId, docPos, score, queryPos)，
    docId: 结果所在文章序号
    docPos: 为三元组，标记结果句位置。第一个元素为行号（段号），第二、三个元素为起止位置
    score: 相似度
    queryPos: 与docPos相似，是对应查询文本的位置
    """

    queryPos, queryText, queryVec = lines2data(lines)
    answer = []

    docId = []
    docPos = []
    docVec = []

    for tar in tars:
        index = np.where(database['id'] == tar)[0].tolist()
        docId += [tar] * len(index)
        docPos += [database['pos'][i] for i in index]
        docVec.append(database['vec'][index])

    docVec = np.vstack(docVec)
    scores = np.dot(docVec, queryVec.T)

    for j in range(scores.shape[1]):
        index = np.where(scores[:, j] > thres)[0].tolist()
        if len(index) > k:
            index = np.argsort(-scores[:, j])[:k].tolist()
        for i in index:
            answer.append((docId[i], docPos[i], scores[i, j], queryPos[j]))

    return answer


def parse(answers, lines):
    """
    :param answers: duplicateCheck的返回值
    :param lines: 与duplicateCheck的参数相同
    :return:
    字典，key为查询文本的位置三元组，value服从要求，附带信息为相似度
    """
    response = {}
    for answer in answers:
        docId, docPos, score, queryPos = answer
        if queryPos not in response.keys():
            response[queryPos] = [None, None, []]
            response[queryPos][0] = lines[queryPos[0]]
            response[queryPos][1] = queryPos[1:]

        index = np.where(database['id'] == docId)[0].tolist()
        string = ""
        for i in index:
            if database['pos'][i][0] == docPos[0]:
                string += database['text'][i]

        response[queryPos][2].append((string, str(score), docPos[1:]))

    return response


if __name__ == "__main__":
    ori = "我  爱  你， 就像  老鼠    爱大米。天天不吃饭"
    text, pos = splitPara(ori)
    print(len(ori))
    print(text)
    print(pos)
