from libs.auxHelpers import returnCount

class System:
    reservedTags = 11
    energy = 50
    mb = 68

class PullField:
    blogid = 0
    blogname = 1
    blogurl = 2
    totalposts = 3
    lastupdate = 4
    posttitle = 5
    postpublished = 6
    postcontent = 7

class Gender:
    female = 0
    male = 1

class Species:
    abandoned = 0
    system = 1
    visitor = 2
    predator = 3
    forager = 4
    dead = 5

class Tags:
    protected = 1
    birth = 2
    death = 3
    starvation = 4
    predation = 5
    grazing = 6
    friends = 7
    comment = 8
    interest = 9
    tag = 10
    trail = 11
    