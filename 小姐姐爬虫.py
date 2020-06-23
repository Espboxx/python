"""请求网页"""
import time

import requests
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3970.5 Safari/537.36 '
}
# 获取文章总数
response = requests.get("https://www.vmgirls.com/special/%e5%b0%8f%e5%a7%90%e5%a7%90", headers=headers)
urlPageCont = re.findall('<span class="px-2">文章 (.*?)</span>', response.text)

urlPageCont = int(urlPageCont[-1])

if urlPageCont % 8 == 0:
    urlPageCont = int(urlPageCont / 8)
else:
    urlPageCont = int(urlPageCont / 8 + 1)
# 当前页面
urlPage = 1
# 计算全部图片
contImg = 0

# 设置请求页面
index_url = 'https://www.vmgirls.com/wp-admin/admin-ajax.php'

# 设置post请求数据


# 循环取网页
while urlPage <= urlPageCont:
    print('当前第：' + str(urlPage) + '/' + str(urlPageCont) + '页')
    ajax_Post = {
        'append': 'list-archive',
        'paged': urlPage,
        'action': 'ajax_load_posts',
        'query': '小姐姐',
        'page': 'tax',
    }
    # 获取网页信息
    response = requests.post(index_url, data=ajax_Post, headers=headers)
    html_text = response.text
    html_urls = re.findall('<a href="(.*?)" class="list-title text-md h-2x" target="_blank">.*?</a>', html_text)

    # 分割地址
    for html_url in html_urls:
        # 重置计数
        cont = 0
        img_html = html_url
        # 图片链接页面
        response = requests.get(img_html, headers=headers)
        # 获取标题
        dir_name = re.findall('<h1 class="post-title h3">(.*?)</h1>', response.text)[-1]
        print(dir_name + "---开始下载")
        # 判断是否存在该图片标题文件夹 如果不存在就创建
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        img_urls = re.findall('<img .*? data-src="(.*?)" data-nclazyload="true">', response.text)
        # 分割图片链接
        for img_url in img_urls:
            cont = cont + 1
            # 分割图片链接获取最后一个下标值
            img_name = img_url.split('/')[-1]
            if (img_name != '2019122813251298.jpg') & (img_name != '2019122813253959.jpg'):

                print('开始下载' + str(cont) + '/' + str(len(img_urls)) + '图片')
                # 读取图片
                response = requests.get(img_url, headers=headers)
                # 写入文件
                with open(dir_name + '/' + img_name, 'wb') as f:
                    f.write(response.content)
                print('图片' + img_name + '下载完成')
                contImg = contImg + 1
            else:
                print(str(cont) + '/' + str(len(img_urls))+'广告不爬取')
    urlPage = urlPage + 1
print('下载完成一共'+str(contImg)+'张图片')
