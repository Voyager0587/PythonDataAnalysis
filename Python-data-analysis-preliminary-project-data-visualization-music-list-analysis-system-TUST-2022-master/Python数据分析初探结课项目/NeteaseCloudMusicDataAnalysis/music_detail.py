"""数据获取，获取歌单详情页的信息"""
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import redis

# 连接到 Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# 定义任务队列和已完成任务集合的键名
URL_QUEUE_KEY = 'url_queue'
VISITED_URLS_KEY = 'visited_urls'

# 加载音乐列表数据
df = pd.read_csv('./music_data/music_list.csv', header=None, on_bad_lines='skip',
                 names=['url', 'title', 'play', 'user'])


def enqueue_url(url):
    """将任务 URL 推入 Redis 队列"""
    r.lpush(URL_QUEUE_KEY, url)


def is_url_visited(url):
    """检查 URL 是否已访问过"""
    return r.sismember(VISITED_URLS_KEY, url)


def mark_as_visited(url):
    """标记 URL 为已访问"""
    r.sadd(VISITED_URLS_KEY, url)


def crawl_music_list_detail(url, headers):
    """爬取音乐列表详情页的信息"""
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 获取歌单标题
    title = soup.select('h2')[0].get_text().replace(',', '，')

    # 获取标签
    tags = []
    tags_message = soup.select('.u-tag i')

    for p in tags_message:
        tags.append(p.get_text())

    # 对标签进行格式化
    if len(tags) > 1:
        tag = '-'.join(tags)
    elif len(tags):
        tag = tags[0]
    else:
        tag = '无'

    # 获取歌单介绍
    if soup.select('#album-desc-more'):
        text = soup.select('#album-desc-more')[0].get_text().replace('\n', '').replace(',', '，')
    else:
        text = '无'

    # 获取歌单收藏量
    collection = soup.select('#content-operation i')[1].get_text().replace('(', '').replace(')', '')

    # 歌单播放量
    play = soup.select('.s-fc6')[0].get_text()

    # 歌单内歌曲数
    songs = soup.select('#playlist-track-count')[0].get_text()

    # 歌单评论数
    comments = soup.select('#cnt_comment_count')[0].get_text()

    # 输出歌单详情页信息
    print('\r', title, tag, text, collection, play, songs, comments, end='', flush=True)

    # 将详情页信息写入CSV文件中
    with open('./music_data/music_detail.csv', 'a+', encoding='utf-8-sig') as f:
        f.write(title + ',' + tag + ',' + text + ',' + collection + ',' + play + ',' + songs + ',' + comments + '\n')



def crawl_music_list_musics(url, headers):
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 获取歌单内歌曲名称
    li = soup.select('.sgchfl .f-thide')

    for j in li:
        # print(j.get_text())
        with open('./music_data/music_name.csv', 'a+', encoding='utf-8-sig') as f:
            f.write(j.get_text().replace(",", " ") + '\n')


def get_data_of_music_list_detail_page():
    """执行爬虫任务"""
    print("正在获取歌单详情页的信息...")
    headers_chrome = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 '
    }

    headers_iphone = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
                      'Version/6.0 Mobile/10A5376e Safari/8536.25'
    }
    for url in df['url']:
        if not is_url_visited(url):
            enqueue_url(url)

    while True:
        url_bytes = r.rpop(URL_QUEUE_KEY)
        if not url_bytes:
            break  # 如果队列为空，则退出循环
        # 将二进制数据解码为字符串
        url = url_bytes.decode('utf-8')  # 假设使用的是 UTF-8 编码，根据实际情况进行修改
        crawl_music_list_detail('https://music.163.com' + url, headers_chrome)
        crawl_music_list_musics('https://music.163.com' + url, headers_iphone)

    print("\n已获取歌单详情页的信息，保存至 music_data/music_name.csv")


