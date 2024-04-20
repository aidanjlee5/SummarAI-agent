from googlesearch import search
from bs4 import BeautifulSoup
import requests

"""
query ="site:https://sciencedaily.com/releases"

#Science articles queries: https://www.science.org/content/article/, sciencedaily.com/releases, sciencenews.org/article
sciencearticles=[""]
for j in search(query, num=10, stop=10, pause=2):
    sciencearticles.append(j)
    
print(sciencearticles)
"""

url = 'https://www.sciencedaily.com/releases/2024/04/240418165151.htm'
page = requests.get(url)
htmlcode = BeautifulSoup(page.text, 'html.parser')
p_tags = htmlcode.find_all('p')
for p in p_tags:
    print(p.text)