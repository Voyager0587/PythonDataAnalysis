"""数据可视化，歌单贡献 UP 主 TOP10"""
import pandas as pd
import matplotlib.pyplot as plt
import time


def data_visualization_of_top_10_song_up():
    """歌单贡献 UP 主 TOP10"""
    # df = pd.read_csv('./music_data/music_name.csv', header=None, on_bad_lines=None, names=['url', 'title', 'play',
    #                                                                                        'user'])
    df = pd.read_csv('./music_data/music_name.csv', header=None, on_bad_lines='skip', names=['url', 'title', 'play',
                                                                                             'user'])
    print("正在生成歌单贡献 UP 主 TOP10 图片...")

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

    # 数据聚合分组
    place_message = df.groupby(['user'])
    place_com = place_message['user'].agg(['count'])
    place_com.reset_index(inplace=True)
    place_com_last = place_com.sort_index()
    dom = place_com_last.sort_values('count', ascending=False)[0:10]

    # 设置显示数据
    names = [i for i in dom.user]
    names.reverse()
    nums = [i for i in dom['count']]
    nums.reverse()
    data = pd.Series(nums, index=names)

    # 设置图片显示属性,字体及大小
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['font.size'] = 10
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
    lines.spines['left'].set_color((64 / 255, 64 / 255, 64 / 255))
    lines.spines['bottom'].set_color((64 / 255, 64 / 255, 64 / 255))

    # 设置坐标轴刻度
    lines.xaxis.set_ticks_position('none')
    lines.yaxis.set_ticks_position('none')

    # 绘制柱状图,设置柱状图颜色
    data.plot.barh(ax=ax, width=0.7, alpha=0.7, color=(153 / 255, 0 / 255, 102 / 255))

    # 添加标题,设置字体大小
    ax.set_title('歌单贡献UP主 TOP10', fontsize=18, fontweight='light')

    # 添加歌曲出现次数文本
    for x, y in enumerate(data.values):
        plt.text(y + 0.3, x - 0.12, '%s' % y, ha='center')

    # 保存图片
    plt.savefig('./music_image/top_10_song_up.png', dpi=None)

    # 显示图片
    plt.show()

    print("\n已生成歌单贡献 UP 主 TOP10 图片，保存至 music_image/top_10_song_up.png")
