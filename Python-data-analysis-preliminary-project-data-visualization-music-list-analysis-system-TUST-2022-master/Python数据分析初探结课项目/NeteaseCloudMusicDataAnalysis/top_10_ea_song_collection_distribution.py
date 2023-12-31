"""数据可视化，欧美歌单收藏数量分布情况"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


def data_visualization_of_top_10_ea_song_collection_distribution():
    """欧美歌单收藏数量分布情况"""
    df = pd.read_csv('./music_data/music_detail.csv', header=None)

    print("正在生成欧美歌单收藏数量分布情况图片...")

    # 输出进度条
    t = 60
    start = time.perf_counter()

    for i in range(t + 1):
        finsh = "▓" * i
        need_do = "-" * (t - i)
        progress = (i / t) * 100
        dur = time.perf_counter() - start

        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")

        time.sleep(0.02)

    # 对收藏数取对数
    dom = []
    for i in df[3]:
        if i != '收藏':  # 检查是否为 '收藏' 字符串
            try:
                dom.append(np.log(int(i.replace('万', '0000'))))
            except ValueError:
                # 如果无法转换为整数，则将其舍弃或做其他处理
                pass
        else:
            # 如果是 '收藏' 字符串，则跳过这个数据点
            pass

    # 确保 dom 列表的长度与 DataFrame 的长度一致
    if len(dom) < len(df):
        # 如果 dom 列表长度小于 DataFrame 的长度，则补充缺失值
        dom.extend([np.nan] * (len(df) - len(dom)))

    # 添加 'collection' 列到 DataFrame
    df['collection'] = dom[:len(df)]  # 只取与 DataFrame 长度相匹配的部分

    # 设置图片显示属性,字体及大小
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.unicode_minus'] = False

    # 设置图片显示属性
    plt.figure(figsize=(16, 8), dpi=80)
    ax = plt.subplot(1, 1, 1)
    ax.patch.set_color('white')

    # 设置坐标轴属性
    lines = plt.gca()

    # 设置坐标轴颜色
    lines.spines['right'].set_color('none')
    lines.spines['top'].set_color('none')
    lines.spines['left'].set_color((64/255, 64/255, 64/255))
    lines.spines['bottom'].set_color((64/255, 64/255, 64/255))
    lines.xaxis.set_ticks_position('none')
    lines.yaxis.set_ticks_position('none')

    # 绘制直方图,设置直方图颜色
    ax.hist(df['collection'], bins=30, alpha=0.7, color=(21/255, 47/255, 71/255))
    ax.set_title('欧美歌单收藏数量分布情况', fontsize=20)

    # 保存图片
    plt.savefig('./music_image/top_10_ea_song_collection_distribution.png', dpi=None)

    # 显示图片
    plt.show()

    print("\n已生成欧美歌单收藏数量分布情况图片，保存至 music_image/top_10_ea_song_collection_distribution.png")
