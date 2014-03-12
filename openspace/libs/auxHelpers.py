from settings.common import DJANGO_ROOT
import os
import fnmatch

def getUpdateCounts():
    """Creates text files out of number of .jpgs in assets directories. CAN ONLY BE RUN LOCALLY"""
    assetspath = os.path.join(DJANGO_ROOT, 'assets/media')
    outpath = os.path.join(DJANGO_ROOT, 'libs/data/assetcounts')
    for folder in os.listdir(assetspath):
        count = len(fnmatch.filter(os.listdir(os.path.join(assetspath, folder)), '*jpg'))
        outfilename = os.path.join(outpath, folder + 'Count.txt')
        with open(outfilename, 'w') as outfile:
            outfile.write(str(count))

def returnCount(species):
    """Returns an int of counts of .jpg assets from files"""
    countpath = os.path.join(DJANGO_ROOT, 'libs/data/assetcounts/' + species + 'Count.txt')
    with open(countpath, 'r') as myfile:
        count = myfile.read()
    return int(count)