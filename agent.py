import supabase_operations
import os
import time
from datetime import datetime, timedelta
import pytz
from supabase import create_client, Client
from dotenv import load_dotenv, find_dotenv
import instructor
from pydantic import BaseModel
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

# Create openai client
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_KEY)
#client = instructor.from_openai(OpenAI()) #Change the naming, maybe?

# Create supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)





"""
#Helper function to test the timer
def send_message():
    print("Message sent!")

def timer(seconds):
    while True:
        time.sleep(seconds)
        send_message()

"""
def insert_db(db, url, topic):
    heading = get_heading(url)
    article_text = get_article_text(url)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an impartial assistant."},
            {"role": "system", "content": get_article_text(url)},
            {"role": "user", "content": "Summarize the following article for me"},
        ]
    )
    gpt_output = response.choices[0].message.content
    if (gpt_output != "I apologize, but I can't provide a summary of the article as you have not provided the text or title of the article. If you provide me with the article's content or its title, I'd be happy to help summarize it for you."):
        supabase_operations.insert_data(db, heading, gpt_output, topic, url)

#Get the date for recent news
def get_current_time():
    current_time = datetime.now()
    my_timezone = pytz.timezone('GMT')
    current_time_my_timezone = current_time.astimezone(my_timezone)
    three_weeks_ago = current_time - timedelta(weeks=2)
    time_str = three_weeks_ago.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    lower_bound_time = (time_str[:10])
    return lower_bound_time


#Used to return the string using the website and topic and date
def query(website, topic):
    three_weeks_ago = get_current_time()[:10]
    search_results = "site:https://www." + website + " " + topic + " after:" + three_weeks_ago
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

def get_heading(url):
    page = requests.get(url)
    htmlcode = BeautifulSoup(page.text, 'html.parser')
    h1_tags = htmlcode.find_all('h1')
    article_text = ''
    for h1 in h1_tags:
        article_text += h1.text
    return article_text

#Function to get the article text from the website



politics_websites = ["cnn.com", "apnews.com/", "nbcnews.com/", "time.com/", "cbsnews.com/"]
sports_websites = ["cbssports.com", "bleacherreport.com", "si.com"]
tech_websites = ["theverge.com", "wired.com", "arstechnica.com"]
health_websites = ["medicalnewstoday.com", "news-medical.net/", "health.harvard.edu"]


"""for politics in politics_websites:
    politics_url=google_search(query(politics, "politics", "2024-04-01"))
    for url in politics_url:
        insert_db(supabase, url, "Politics")

"""

"""for sports in sports_websites:
    sports_url=google_search(query(sports, "sports", "2024-04-01"))
    for url in sports_url:
        insert_db(supabase, url, "Sports")"""


"""for tech in tech_websites:
    tech_url=google_search(query(tech, "tech", "2024-04-01"))
    for url in tech_url:
        insert_db(supabase, url, "Tech")
"""

for health in health_websites:
    health_url=google_search(query(health, "health"))
    for url in health_url:
        insert_db(supabase, url, "Health")
