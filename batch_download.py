#!python3
from bs4 import BeautifulSoup
import requests
import re
from optparse import OptionParser
import os

#PROJECT MANAGEMENT
# Features to add:
# X Strip URL and save as URL name file
# X Command line options
# - Parallel downloads
# - Progress bars
# - Logins so I can download from Canvas, etc.

# Set up command line options
parser = OptionParser()
parser.add_option("-d", "--dir", dest="outputDir", action="store", default=".",
        help="The directory where the files should be downloaded")
parser.add_option("-e", "--extension", dest="extensions", action="append", default=[],
        help="The extension (without the leading .) you want the script to download")
parser.add_option("-u", "--url", dest="websiteUrl", action="store",
        help="The URL you want to scrape")
(options, args) = parser.parse_args()

def getWebsiteRoot(websiteUrl, relativeUrl):
    # Makes a relative URL an absolute one given the base page URL.
    rootEnd = websiteUrl.rfind('/')
    websiteRoot = websiteUrl[0 : rootEnd + 1]
    relative = relativeUrl
    if relative[0] == '.':
        relative = relative[1:len(relative)]
    if relative[0] == '/':
        relative = relative[1:len(relative)]
        
    return websiteRoot + relative


websiteUrl = options.websiteUrl
extensions = options.extensions

website = requests.get(websiteUrl)
print(website);

soup = BeautifulSoup(website.content, 'html.parser')
#print(soup.text)
#print(soup.a)

allAnchors = soup.find_all('a')
for a in allAnchors:
    allDownloads = []
    for extension in extensions:
        allAnchors = soup.find_all('a')
        for a in allAnchors:
            if 'href' in a.attrs:
                matches = re.findall(r".*\.%s.*" %extension, a.attrs['href'])
                if matches:
                    allDownloads.append(matches[0])


#Print the files to download
print("-----------------------------------------------------")
print("Files to download:")
print("-----------------------------------------------------")
for url in allDownloads:
    if (url[0:4] != "http"):
        url = getWebsiteRoot(websiteUrl, url)
    print(url)
    beginningOfFileName = url.rfind('/')
    fileName = url[beginningOfFileName + 1 : len(url)]

    # Remove anything after the extension
    endOfExtension = fileName.find(extension)
    fileName = fileName[0:endOfExtension + len(extension)]
    fileName = os.path.join(options.outputDir, fileName)

    print("Downloading %s...." %fileName, end='')
    file = requests.get(url);
    print("Done. Saving...", end='')
    
    open("%s"  %fileName, 'wb').write(file.content);
    print("Done.")

