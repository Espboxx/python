import requests
import json
import re
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3970.5 Safari/537.36 '
}
cont = 1;



def change_title(title):
    pattern = re.compile(r"[\/\\\:\*\?\"\<\>\|]")
    new_title = re.sub(pattern, "_", title)
    return new_title


def dow(video_title, video_url):
    print('正在下载:' + video_title)
    video_data = requests.get(video_url, headers=headers).content
    with open('video/' + video_title, 'wb') as f:
        f.write(video_data)
        print('下载完成...')


def t1():
    for page in range(1, 228):
        print('正在抓取第{}页数据'.format(str(page)))

        base_url = 'http://v.6.cn/minivideo/getlist.php?act=recommend&page={}&pagesize=20'.format(str(page))

        response = requests.get(base_url, headers=headers)
        response_data = response.text
        # 转换数据
        dict_data = json.loads(response_data)
        data_list = dict_data['content']['list']
        for data in data_list:
            video_title = data['title'] + '.mp4'  # 视频文件名
            video_title = change_title(video_title)
            video_url = data['playurl']
            while threading.active_count() > 50:
                pass

            threading.Thread(target=dow, args=(video_title, video_url)).start()
t1()