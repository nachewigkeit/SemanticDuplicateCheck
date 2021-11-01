# 基于Sentence Bert的语义查重

通过Sentence Bert将句子转化为向量，两句向量相似度高于阈值即判定为重复。我们希望这样可以避免抄袭者不改变句意仅修改表达方式就骗过查重系统。



config.py: 配置路径

main.py: 启动应用

buildDatabase.py: 建立数据库

client.py: 主要函数库

train/evaluate.py 绘制ROC曲线评测模型

train/fine_tune.py 微调模型

train/translate.py 通过循环翻译构造正例数据

