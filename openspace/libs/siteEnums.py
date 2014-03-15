from libs.auxHelpers import returnCount

class System:
    reservedTags = 7

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
    profile_tag = 10
    post_tag = 11
    trail = 12
    
class Notification:
    no_notification = 0
    birth = 1
    death = 2
    starvation = 3
    predation = 4
    grazing = 5
    made_friend = 6
    comment = 7
    interest = 8
    profile_tag = 9
    post_tag = 10
    trail = 11
    nope = 12
    