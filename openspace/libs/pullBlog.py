from random import randint
import os
import data_path

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

def pullBlog(blog):
    blogs = fileRead(os.path.join(data_path.DATA_PATH, "recoveredBlogs.txt")).split("[*START-BLOG*]")
    if not blog:
        blog = randint(0, len(blogs)-1)
        while int(getField(3, blogs[blog])) < 3:
            blog = randint(0, len(blogs)-1)
    blogId = str(blog)
    returnPosts = []
    url = getField(2, blogs[blog])
    posts = blogs[blog].split("[*START-POST*]")
    lastUpdate = getField(6, posts[1])
    for post in posts[1:]:
        if post != "" and post != u"\u000D":
            tp = [getField(5, post), getField(6, post), getField(7, post)]
            returnPosts.append(tp)
    
    return blogId, url, lastUpdate[:10], returnPosts