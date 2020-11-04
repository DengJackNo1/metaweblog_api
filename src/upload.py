#! /usr/bin/env python
# coding=utf-8
import os
import asyncio
import html
import xmlrpc.client
import glob
from src.img_transfer import *
from .config import *

# 创建路径
for path in [art_path, unp_path, bak_path]:
    if not os.path.exists(path):
        os.makedirs(path)

net_images = []  # 图片上传后url
image_count = 1  # 图片计数


def get_image_url(t):
    """回调，获取url"""
    global image_count
    url = t.result()['url']
    print(f'第{image_count}张图片上传成功,url:{url}')
    net_images.append(url)
    image_count += 1


def process_img(mdfile):
    with open(mdfile, encoding='utf-8') as f:
        md = f.read()

    print(f'markdown读取成功:{mdfile}')
    local_images = find_md_img(md)
    if local_images:  # 有本地图片，异步上传
        tasks = []
        for li in local_images:
            image_full_path = li
            task = asyncio.ensure_future(upload_img(image_full_path))
            task.add_done_callback(get_image_url)
            tasks.append(task)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        image_mapping = dict(zip(local_images, net_images))

        md = replace_md_img(mdfile, image_mapping)
    else:
        print(f'{mdfile}无需上传图片')


def upload():
    for mdfile in glob.glob(art_path + "*.md"):
        title = os.path.basename(mdfile)  # 获取文件名做博客文章标题
        [title, _] = os.path.splitext(title)  # 去除扩展名

        # 处理markdown文件中的图片
        process_img(mdfile)


        post = dict(description=md, title=title, categories=['[Markdown]'])
        recent_posts = server.metaWeblog.getRecentPosts(conf["blog_id"], conf["username"], conf["password"], recentnum)
        # 获取所有标题，需要处理HTML转义字符
        recent_posts_titles = [html.unescape(recent_post['title']) for recent_post in recent_posts]
        if title not in recent_posts_titles:
            server.metaWeblog.newPost(conf["blog_id"], conf["username"], conf["password"], post, conf["publish"])
            print(f"markdown上传成功, 博客标题为'{title}', 状态为'未发布', 请到博客园后台查看")
        elif input('博客已存在, 是否更新?(y/n)') == 'y':
            for recent_post in recent_posts:
                if title == recent_post['title']:
                    update_post = recent_post
                    update_post['description'] = md
                    try:
                        server.metaWeblog.editPost(update_post['postid'], conf["username"], conf["password"],
                                                   update_post,
                                                   False)
                    except xmlrpc.client.Fault as fault:
                        if 'published post can not be saved as draft' in str(fault):
                            server.metaWeblog.editPost(update_post['postid'], conf["username"], conf["password"],
                                                       update_post, True)
                        else:
                            raise fault
                    print(f"博客'{title}'更新成功")
        else:
            print('上传已取消')



