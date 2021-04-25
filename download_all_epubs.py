#!python3
from bs4 import BeautifulSoup
import requests
import re

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
num=1
print("-----------------------------------------------------")
print("Files to download:")
print("-----------------------------------------------------")
for url in allDownloads:
    print(url)
    continue
    file = requests.get(url);
    open("download%d.%s" %num %extension, 'wb').write(file.content);
    num = num + 1

