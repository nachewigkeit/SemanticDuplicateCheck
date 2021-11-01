import config
from client import duplicateCheck, parse

with open(config.newTextPath, "r", encoding="utf-8") as f:
    lines = f.readlines()

tar = list(range(1, 17))
answers = duplicateCheck(lines, tar, 0.6, 3)
response = parse(answers, lines)
for i in response.values():
    print(i[0])
    for j in i[2]:
        print(j[0][j[2][0]:j[2][1]])
