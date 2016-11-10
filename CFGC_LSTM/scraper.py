#Michelle Morales
#Collect crossfit data from www.crossfitgardencity.com
#Use Crossfit Garden City's WOD blog and DCGAN to automatically generate new crossfit WODs

import urllib2, re
from bs4 import BeautifulSoup as bs

# http://crossfitgardencity.com/wod/2000/ #March 13, 2014
# http://crossfitgardencity.com/wod/1000/ #April 22, 2011

for x in range(1000,2001):
    #open page, parse html, pull info from tree
    page = urllib2.urlopen('http://crossfitgardencity.com/wod/%s/'%str(x)).read()
    tree = bs(page)
    title = tree.title.string
    date = title.split('|')[1].strip().replace(',','').replace(' ','_')
    newF = open('CFGC_data/%s.txt'%date,'w')
    text = tree.get_text()
    try:
        #Only save WOD if we can right pattern if not continue onto the next page
        start = re.search("Workout of the Day", text).start()
        end = re.search('Leave a Comment', text).start()
        WOD = text[start:end].strip()
        print date
        print WOD
        print '----------------------------'
        newF.write(WOD.encode('ascii','ignore'))
    except:
        continue
