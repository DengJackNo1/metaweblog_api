#!/usr/bin/python
# encoding:utf-8

conf = {
    'blog_url': "https://rpc.cnblogs.com/metaweblog/deng1821333144",
    'blog_id': "505485",
    'username': "1821333144",
    "appkey": "deng1821333144",
    'password': "199443deng",
    # 是否生成图片替换后本地文件,默认False关闭
    'gen_network_file': False,
    # 上传后是否发布，默认未发布，设置True为发布
    'publish': False,
    # 图片自定义显示格式，默认不设置
    # 如设置width和居中，<center><img src:"{}" style:"width:100%" /></center>
    'img_format': ""
}


# 发布文章路径(article path)
art_path = "./articles/"
# 不发布文章路径(unpublished article path)
unp_path = "./unpublished/"
# 博客配置路径(config path)
cfg_path = "blog_config.json"
# 备份路径(backup path)
bak_path = "./backup/"
# 获取文章篇数
recentnum = 999