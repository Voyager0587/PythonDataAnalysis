"""数据可视化，歌单介绍词云图"""
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
import jieba
import time


def data_visualization_of_music_wordcloud():
    """歌单介绍词云图"""
    df = pd.read_csv('./music_data/music_detail.csv', header=None)
    text = ''

    print("正在生成歌单介绍词云图片...")

    # 输出进度条
    t = 60
    start = time.perf_counter()  # 调用一次 perf_counter()，从计算机系统里随机选一个时间点 A，计算其距离当前时间点B1有多少秒。
    # 当第二次调用该函数时，默认从第一次调用的时间点 A 算起，距离当前时间点B2有多少秒。两个函数取差，即实现从时间点B1到B2的计时功能。

    for i in range(t + 1):
        finsh = "▓" * i  # i 个长度的 * 符号
        need_do = "-" * (t - i)
        progress = (i / t) * 100  # 显示当前进度，百分之多少
        dur = time.perf_counter() - start

        # \r是一个转义字符，用来在每次输出完成后，将光标移至行首，这样保证进度条始终在同一行输出，即在一行不断刷新的效果；
        # {:^3.0f}，输出格式为居中，占3位，小数点后0位，浮点型数，对应输出的数为c；{}，对应输出的数为a；{}，对应输出的数为b；
        # {:.2f}，输出有两位小数的浮点数，对应输出的数为dur；end=''，用来保证不换行，不加这句默认换行。
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")

        time.sleep(0.02)  # 在输出下一个百分之几的进度前，停止0.2秒

    for line in df[2]:
        text += ' '.join(jieba.cut(line, cut_all=False))

    background_image = plt.imread('./music_image/background_image.jpg')

    stopwords = set('')
    stopwords.update(
        ['封面', 'none介绍', '介绍', '歌单', '歌曲', '我们', '自己', '没有', '就是', '可以', '知道', '一起', '不是',
         '因为', '什么', '时候', '还是', '如果', '不要', '那些', '那么', '那个', '所有', '一样', '一直', '不会', '现在',
         '他们', '这样', '最后', '这个', '只是', '有些', '其实', '开始', '曾经', '所以', '不能', '你们', '已经', '后来',
         '一切', '一定', '这些', '一些', '只有', '还有', '的', '和', '我', '你', '了', '都', '是', '里', '在', '与',
         '就', '让', '个', '也', '而', '着', '为', '能', '有', '会', '中', '到'])

    wc = WordCloud(
        background_color='white',
        mask=background_image,
        font_path='./font_resources/STZHONGS.ttf',
        max_words=2000,
        max_font_size=150,
        random_state=30,
        stopwords=stopwords
    )
    # stopwords :设置停用词，这些词会在生成词云时被过滤掉，不会出现在词云图中。
    # random_state 参数用于控制词云生成过程中的随机性，设置了种子值可以使得每次生成的词云图相同。
    wc.generate_from_text(text)
    # generate_from_text() 方法会根据输入的文本内容绘制词云图，词语出现频率较高的部分会以更大的字体、更醒目的样式展现在词云图中，而出现频率较低的词语则会以相对较小的字体展示。

    # 看看词频高的有哪些,把无用信息去除
    process_word = WordCloud.process_text(wc, text)  # 将长文本拆分为单词，消除停顿词。
    # process_text函数主要用于对文本进行预处理，包括分词、去除停用词、去除标点符号等操作。
    # process_text函数返回的结果是一个字典，其中包含了分词后的token以及对应出现的次数。

    # 用来看看词云的前五十有什么词，消除一些没用的
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    # print(sort[:50])

    img_colors = ImageColorGenerator(background_image, default_color=(255, 255, 255))

    # ImageColorGenerator 是 WordCloud 库中的一个类，用于根据指定的图片生成颜色对象，以便在词云图中为每个词汇选择相应的颜色。

    wc.recolor(color_func=img_colors)
    # 通过 recolor() 方法，你将之前创建的颜色生成器对象 img_colors 应用到词云图对象 wc 上。这个操作会使用 img_colors 对象中提供的颜色信息，为词云图中的各个词汇选择相应的颜色。
    # 根据背景图片的颜色信息，为词云图中的每个词汇分配适当的颜色。这样做可以让词云图的词汇颜色更贴近于背景图片的色调，使得整个图像看起来更加和谐统一。
    plt.imshow(wc)  # 显示词云图 wc，将生成的词云图展示在当前的 Matplotlib 图形环境中，相当于放到Matplotlib 图形环境中
    plt.axis('off')  # 隐藏了词云图中的坐标轴，使得在显示词云图时不会显示坐标轴。

    # 保存图片
    wc.to_file("./music_image/music_wordcloud.png")

    # 显示图片
    plt.show()

    print("\n已生成歌单介绍词云图片，保存至 music_image/music_wordcloud.png")
