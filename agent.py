import supabase_operations
import os
import time
from datetime import datetime, timedelta
import pytz
from supabase import create_client, Client
from dotenv import load_dotenv
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from googlesearch import search
from bs4 import BeautifulSoup
import requests


# https://supabase.com/docs/reference/python/installing
# https://github.com/openai/openai-python/discussions/1071
# https://pypi.org/project/instructor/
# https://pypi.org/project/python-dotenv/

"""API_KEY=open(".env.local", "r").read()
#OpenAI.api_key = API_KEY
print(API_KEY[11:])
client = OpenAI(
    api_key = API_KEY,
)"""

load_dotenv('.env.local')

class SummmarizeArticle(BaseModel):
    headline: str = Field(..., title="Headline", description="A concise description of the entire article in a single sentence, where the main purpose is to provide a brief overview of the article.")
    summary: str = Field(..., title="Summary", description="A summarized version of the article, try to avoid any bias and provide a neutral summary of the article. Never include the clause: The article is about, the article discusses, the article talks about, etc. Instead just summarize the content")
    successfullySummarized: bool = Field(..., title="successfullySummarized", description="A boolean value that indicates whether an article text was found, if the article text is coherent and a summary was successfully generated, and if there's only one article being summarized, then this value should be true")
    isAnArticle: bool = Field(..., title="isAnArticle", description="A boolean value that indicates whether the text is an article or not. If the text contains any sort of copyright information, provides updates on the topic but doesn't discuss any content, orx` does not have any information that is similar to a news article, then this value should be false.")
    topic: str = Field(..., title="Topic", description="The category the article belongs to: Politics, Sports, Technology, Health, etc. Try to only include the categories: Politics, Sports, Technology, Health, etc. The category should never be just 'news'. If a category is short for another category (i.e tech being short for technology), only include the longer category name")


# Create openai client
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
client = instructor.from_openai(OpenAI(api_key=OPENAI_KEY))
#client = instructor.from_openai(OpenAI()) #Change the naming, maybe?

# Create supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_db(db, url):
    #heading = get_heading(url)
    article_text = get_article_text(url)
    if (len(article_text) > 0):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model = SummmarizeArticle,
            messages=[
                {"role": "system", "content": "You are an impartial assistant."},
                {"role": "system", "content": get_article_text(url)},
                {"role": "user", "content": "Summarize the following article for me"},
            ]
            
        )
        #gpt_output = response.choices[0].message.content
        if (response.successfullySummarized != False or response.isAnArticle != False):
            supabase_operations.insert_data(db, response.headline, response.summary, response.topic, url)

#Get the date for recent news
def get_current_time():
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    lower_bound_time = (time_str[:10])
    return lower_bound_time


#Used to return the string using the website and topic and date
def query(website, topic):
    current_time = get_current_time()[:10]
    search_results = "site:https://www." + website + " " + topic + " after:" + current_time
    return search_results
        
#Function to search google for articles
def google_search(query):
    search_results = []
    for j in search(query, num=10, stop=10, pause=2):
        search_results.append(j)
    return search_results 

#Function to scrape the article text from the websites
def get_article_text(url):
    page = requests.get(url)
    htmlcode = BeautifulSoup(page.text, 'html.parser')
    p_tags = htmlcode.find_all('p')
    article_text = ''
    for p in p_tags:
        article_text += p.text
    return article_text

#Function to get the article text from the website



politics_websites = ["cnn.com", "apnews.com/", "nbcnews.com/", "time.com/", "cbsnews.com/"]
sports_websites = ["cbssports.com", "bleacherreport.com", "si.com"]
tech_websites = ["theverge.com", "wired.com", "arstechnica.com"]
health_websites = ["medicalnewstoday.com", "news-medical.net/", "health.harvard.edu"]
website_database = [politics_websites, sports_websites, tech_websites, health_websites]

def find_articles_today():
    count=0
    for website_category in website_database:
        for website_url in website_category:
            articles_url = google_search(query(website_url, "news"))
            for url in articles_url:
                insert_db(supabase, url)
                print("inserted summary")
                count+=1
            print(count)

find_articles_today()


"""for politics in politics_websites:
    politics_url=google_search(query(politics, "politics"))
    count=0
    for url in politics_url:
        insert_db(supabase, url)
        print("inserted summary")
        count+=1
    print(count)"""



"""for sports in tech_websites:
    sport_url=google_search(query(sports, "spots"))
    count=0
    for url in sport_url:
        insert_db(supabase, url)
        print("inserted summary")
        count+=1
    print(count)"""


"""for tech in tech_websites:
    tech_url=google_search(query(tech, "tech"))
    count=0
    for url in tech_url:
        insert_db(supabase, url)
        print("inserted summary")
        count+=1
    print(count)"""


"""for health in health_websites:
    count=0
    health_url=google_search(query(health, "health"))
    for url in health_url:
        insert_db(supabase, url)
        print("inserted summary")
        count+=1
    print(count)"""

