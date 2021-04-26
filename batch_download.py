#!python3
from bs4 import BeautifulSoup
import requests
import re

#PROJECT MANAGEMENT
# Features to add:
# - Strip URL and save as URL name file
# - Command line options
# - Parallel downloads
# - Progress bars

def getWebsiteRoot(websiteUrl, relativeUrl):
    # Returns the root of the website in case the URL is relative, not absolute
    rootEnd = websiteUrl.rfind('/')
    websiteRoot = websiteUrl[0 : rootEnd + 1]
    relative = relativeUrl
    if relative[0] == '.':
        relative = relative[1:len(relative)]
    if relative[0] == '/':
        relative = relative[1:len(relative)]
        
    return websiteRoot + relative

websiteUrl="http://classes.ece.usu.edu/3640/resources.html"
website = requests.get(websiteUrl)
print(website);

soup = BeautifulSoup(website.content, 'html.parser')
#print(soup.text)
#print(soup.a)

allAnchors = soup.find_all('a')
for a in allAnchors:
    #print(a)

    allDownloads = []
    extension='pdf'
    allAnchors = soup.find_all('a')
    for a in allAnchors:
        #print(a.string)
        if 'href' in a.attrs:
            #print(a.attrs['href'])
            matches = re.findall(r".*\.pdf.*", a.attrs['href'])
            #print(matches)
            if matches:
                allDownloads.append(matches[0])


#Print the files to download
print("-----------------------------------------------------")
print("Files to download:")
print("-----------------------------------------------------")
for url in allDownloads:
    if (url[0:3] != "http"):
        url = getWebsiteRoot(websiteUrl, url)
    print(url)
    beginningOfFileName = url.rfind('/')
    fileName = url[beginningOfFileName + 1 : len(url)]
    # Remove anything after the extension
    endOfExtension = fileName.find(extension)
    fileName = fileName[0:endOfExtension + len(extension)]
    print("Downloading %s...." %fileName, end='')
    file = requests.get(url);
    print("Done. Saving...", end='')
    
    open("%s"  %fileName, 'wb').write(file.content);
    print("Done.")

