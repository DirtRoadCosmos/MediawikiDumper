import urllib2
import urllib
import cookielib
import re
import sys
import shutil
import os
import csv
from datetime import datetime
from ImageDownloader import ImageDownloader
from HTMLParser import HTMLParser

base = 'http://help.tomtomgroup.com'
iclVersion = sys.argv[1]
print iclVersion
targetBase = sys.argv[2]
print targetBase
pageListFile = sys.argv[3]
print pageListFile

class SaveImages(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="img":
            srcImgPath = (dict(attrs)["src"])
            # print "srcImgPath", srcImgPath
            if "skins" not in srcImgPath:
                srcImgPathFull = base+"/"+srcImgPath
                # print "srcImgPathFull", srcImgPathFull  
                srcImgPathRedo = srcImgPath.replace('/','\\')
                # print "srcImgPathRedo", srcImgPathRedo
                # endpath = os.path.join(targetbase, p2[36:])
                targetPath = os.path.join(targetBase, srcImgPathRedo)
                # print "targetPath", targetPath
                # Get directory name
                targetDir = os.path.dirname(targetPath)
                # print "targetDir", targetDir
                # If the directory exists, download the file directly

                if os.path.isdir(targetDir):
                    # print "exists!"
                    # print base+srcImgPath
                    urllib.urlretrieve(srcImgPathFull, targetPath)
                    # print "saved"
                # Make local directory if it doesn't exist, then dowload file
                else:
                    # print "doesn't exist"
                    os.makedirs(targetDir)
                    # print "now it does!"
                    urllib.urlretrieve(srcImgPathFull, targetPath)
                    # print "saved"
                print "image saved", targetPath


                
#get pagelist

r = csv.reader(open(pageListFile, "rb"))

iclPages = []

for row in r:
    iclPages.append(row[0])
    
# remove spaces in page list
iclPages = [p.replace(' ', '_') for p in iclPages]

#config
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

pageCount = len(iclPages)
print pageCount, "pages to be handled"

thePage = ''
start = datetime.now()

#loop through each page
for i, thePage in enumerate(iclPages):
    pageTitle = ''.join(thePage)
    print 'pageTitle:', pageTitle
    
    # if the pagetitle is given in URL form (getting earlier revision), then extract the shortened form
    if pageTitle[0] == '?':
        matchObj=re.search('(=)([a-zA-Z0-9_\-]*)(&)', pageTitle)
        pageTitleShort = matchObj.group(2)
    else:
        pageTitleShort = pageTitle
    print 'pageTitleShort:', pageTitleShort   

    if cpp == "cpp":
        theUrl = 'http://help.tomtomgroup.com/ttpedia/wiki_solving_methods/index.php/' + pageTitle
    else:
        theUrl = 'http://help.tomtomgroup.com/ttpedia/wiki_icl_' + iclVersion + '/index.php/' + pageTitle        
    request = urllib2.Request(theUrl)

    f = opener.open(request)
    data = f.read()

    p=re.compile("src=\"/ttpedia")
    data=p.sub("src=\"ttpedia", data)

    #write the page
    theFile = open(os.path.join(targetBase,pageTitleShort+'.html'), 'wb')
    theFile.write(data)
    theFile.close()

    print "text saved for", pageTitleShort
    
    #save images    
    h=SaveImages()
    h.feed(data)
    print "images saved for", pageTitleShort
    
    lap = datetime.now()
    timeSinceStart = (lap-start).seconds
    timePerPage = (lap-start)//(i+1)
    pagesDone = i+1
    secRemaining = (timePerPage * (pageCount - (pagesDone))).seconds
    print pagesDone, "of", pageCount, "done", "in", timeSinceStart, "seconds.", secRemaining, "seconds remaining."
    
opener.close()

          
