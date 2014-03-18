from apps.profiles.models import Profile, Post
from libs.profileHelpers import makeBuildAbandoned
import data_path
import os, io

def fileOut(filename, data, mode):
    file = io.open(filename, mode)
    file.write(unicode(data))
    file.close()

def bigBlogBuildout(chunk):
    with open (os.path.join(data_path.DATA_PATH, "buildData/lastBuildId.txt"), "r") as idFile:
        initialBuildId = idFile.read().replace("\n", "")
    blogId = int(initialBuildId)
    for i in range(chunk):
        profile = makeBuildAbandoned(blogId)
        blogId += 1
        if profile:
            result = profile.fullName
        else:
            result = "filtered"
        fileOut(os.path.join(data_path.DATA_PATH, "buildData/buildLog.txt"), str(blogId) + " - " + result + "\n", "a")
        fileOut(os.path.join(data_path.DATA_PATH, "buildData/lastBuildId.txt"), str(blogId), "w")
        