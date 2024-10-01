# summarai-agent
The agent for summarai

Instructions for running the python script

Python packages used - nextjs, pip-install [package]


Goal- running python script- searches all the topics that Summarai requests for, with the intention of updating daily. 

Add support for topics- manually google websites from certain news sources to filter through to articles only, scrape the website, then run the information to chatgpt, then transfer to the data base



TOPICS AND QUERIES USED TO GET CORRESPONDING ARTICLES:

Politics article queries:
    site:https://www.cnn.com politics after:2024-04-01
    site:https://apnews.com/ politics after:2024-04-01
    site:https://www.nbcnews.com/ politics after:2024-04-01
    site:https://time.com/ politics after:2024-04-01
    site:https://www.cbsnews.com/ politics after:2024-04-01

Sports article queries
    site:cbssports.com article after:2024-04-01
    site:bleacherreport.com article after:2024-04-01
    site:si.com story after:2024-04-01

Tech article queries
    site:theverge.com article after:2024-04-01
    site:wired.com tech story after:2024-04-01
    site:arstechnica.com story after:2024-04-01

Health article queries
    site:medicalnewstoday.com articles after:2024-04-01
    site:https://www.news-medical.net/ story after:2024-04-01
    site:https://www.health.harvard.edu stories after:2024-04-01

instructor
1. Google package - beautiful soup package for scraping (Run it once a day ideally)
2. OpenAI package for ChatGPT 4.0 -> Supabase Python client