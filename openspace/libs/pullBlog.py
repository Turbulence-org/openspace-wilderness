from random import randint
import os
import data_path
from libs.siteEnums import PullField

def fileRead(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    return data

def getField(field, data):
    fields = ["BLOG-ID", "BLOG-NAME", "BLOG-URL", "TOTAL-POSTS", "LAST-UPDATE", "POST-TITLE", "POST-PUBLISHED", "POST-CONTENT"]
    sMark = "[*" + fields[field] + "*]"
    eMark = "[*END-" + fields[field] + "*]"
    start = data.index(sMark) + len(sMark)
    if data.count(sMark) > 0:
        end = data.index(eMark, start)
        return data[start:end]
    
def blogsCount():
    blogs = fileRead(os.path.join(data_path.DATA_PATH, "recoveredBlogs.txt")).split("[*START-BLOG*]")
    return count(blogs)

def pullBlog(blog):
    blogs = fileRead(os.path.join(data_path.DATA_PATH, "recoveredBlogs.txt")).split("[*START-BLOG*]")
    if not blog:
        blog = randint(0, len(blogs)-1)
        while int(getField(PullField.totalposts, blogs[blog])) < 3:
            blog = randint(0, len(blogs)-1)
    blogId = str(blog)
    returnPosts = []
    url = getField(PullField.blogurl, blogs[blog])
    posts = blogs[blog].split("[*START-POST*]")
    lastUpdate = getField(PullField.postpublished, posts[1])
    for post in posts[1:]:
        if post != "" and post != u"\u000D":
            tp = [getField(PullField.posttitle, post), getField(PullField.postpublished, post), getField(PullField.postcontent, post)]
            returnPosts.append(tp)
    
    return blogId, url, lastUpdate[:10], returnPosts

def pullBlogFilter(blog):
    blogs = fileRead(os.path.join(data_path.DATA_PATH, "recoveredBlogs.txt")).split("[*START-BLOG*]")
    blogId = str(blog)
    if int(getField(PullField.totalposts, blogs[blog])) > 2:
        returnPosts = []
        url = getField(PullField.blogurl, blogs[blog])
        posts = blogs[blog].split("[*START-POST*]")
        lastUpdate = getField(PullField.postpublished, posts[1])
        for post in posts[1:]:
            if post != "" and post != u"\u000D":
                tp = [getField(PullField.posttitle, post), getField(PullField.postpublished, post), getField(PullField.postcontent, post)]
                returnPosts.append(tp)
    
        return blogId, url, lastUpdate[:10], returnPosts
    return None, None, None, None
        