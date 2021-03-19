import jieba
from utils import normalizeString
# 对英文转小写，去除非法字符
from utils import cht_to_chs
# 繁体转简写
SOS_token = 0
EOS_token = 1
MAX_LENGTH = 10

class Lang:
    def __init__(self, name):
        self.name = name
        # name 定义是中文还是英文
        self.word2index = {}
        # 对词语进行编码
        self.word2count = {}
        # 统计每个词出现的频率
        self.index2word = {
            0:"SOS", 1:"EOS"
            # 起始符和终止符，用于Seq2Seq中解码器开始与结束
        }
        self.n_words = 2
        # 对句子进行编码的处理，初始值为2


    def addWord(self, word):
        # 对词进行统计，利用word来更新索引值
        if word not in self.word2index:
            # 如果词不在索引值中
            self.word2index[word] = self.n_words
            # 就添加索引
            self.word2count[word] = 1
            #
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1
            # 否则词频直接加1

    def addSentence(self, sentence):
        # 对句子进行解析，通过空格进行切分
        for word in sentence.split(" "):
            self.addWord(word)
        #完成了对字典的统计

def  readLangs(lang1, lang2, path):
    # 传入两种文本，分别是中文和英文
    lines = open(path, encoding="utf-8").readlines()
    lang1_cls = Lang(lang1)
    lang2_cls = Lang(lang2)

    pairs = []
    # 对每一条数据进行切分
    for l in lines:
        l = l.split("\t")
        sentence1 = normalizeString(l[0])
        # 进行小写操作
        sentence2 = cht_to_chs(l[1])
        # 繁体转简写
        seg_list = jieba.cut(sentence2, cut_all=False)
        # jieba进行分词
        sentence2 = " ".join(seg_list)

        if len(sentence1.split(" ")) > MAX_LENGTH:
            # 对句子中分词的数量进行限制
            # 如果大于最大限制，过滤长句
            continue

        if len(sentence2.split(" ")) > MAX_LENGTH:
            continue
        pairs.append([sentence1, sentence2])
        # 存入到pairs中

        lang1_cls.addSentence(sentence1)

        lang2_cls.addSentence(sentence2)

    return lang1_cls, lang2_cls, pairs


lang1 = "en"
lang2 = "cn"
path = "data/en-cn.txt"
lang1_cls, lang2_cls, pairs = readLangs(lang1, lang2, path)

print(len(pairs))
print(lang1_cls.n_words)
print(lang1_cls.index2word)

print(lang2_cls.n_words)
print(lang2_cls.index2word)
