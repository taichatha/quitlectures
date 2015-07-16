from lxml import html
import requests
import pafy
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls 
tls.set_credentials_file(username='taic', api_key='wt64g3dn25')

'''
need to be able to crawl an entire space
looks like it's going to be infoco.
We need to find a way to check if youtube is
of the video source.
we can use is 'www.youtube.com' in the string.
once we know it's not in one of the links,
then we can ignore the rest.
we could just get the individual links, but
let's get fancy, and find a way to scrape it.
looks like there is a pattern:
Mathematics: mathematics/mathematics.html
Physics: physics/physics.html
Chemistry and Chemical Engineering:
chemistry/chemisty-and-chemical-engineering.html
so the pattern is (field)/(field)+
(someextraneousstuff)*.html 
'''

'''path for infocobuild
start at infocobuild.com/education/audio-video-courses
go to courses by subject.
Then we go through each School:
only check if it's video/text
then once in each course, check if youtube is the first youtube_clip
if it is, then lets mine this bitch.
if not, ignore this course, and go to the next one.


'''

page = requests.get('http://www.infocobuild.com/education/audio-video-courses/mathematics/18-085-science-and-engineering-i-mitocw.html')
tree = html.fromstring(page.text)
videos = tree.xpath('//a/@href')


for i in videos:
	if 'mathematics/18' not in i:
		videos.remove(i)



for i in videos:
	if 'index.html' in i:
		videos.remove(i)



videos = sorted(videos)
# for i in videos:
# 	print i


print "----"
#open each video link
#get youtube link
#put in pafy
#get viewcount
views = []

#need to make this faster.
#goes on for way too long.
for i in videos:
	check_page = requests.get(str(i))
	videoTree = html.fromstring(check_page.text)
	youtube_clip = videoTree.xpath('//iframe/@src')
	
	if 'www.youtube.com/' in youtube_clip[0]:
		video = pafy.new(youtube_clip[0])
		views.append((video.title, video.viewcount))
		
for i in views:
	print i

#x is the video number for the plot
x=[]
#y is the views
y=[]
for i,v in enumerate(views):
	x.append(i)
	y.append(v[1])

print y
trace1 = Scatter(x=x, y=y)
data = Data([trace1])
plot_url = py.plot(data, filename='plots/18.085')
#go through KhanAcademy
