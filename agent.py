from googlesearch import search

query ="site:https://www.livescience.com/"

#Science articles queries: https://www.science.org/content/article/, sciencedaily.com/releases instructor

for j in search(query, num=10, stop=10, pause=2):
    print(j)