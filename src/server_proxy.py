import xmlrpc.client

from src.config import conf

blog_url = conf["blog_url"].strip()
server = xmlrpc.client.ServerProxy(blog_url)
