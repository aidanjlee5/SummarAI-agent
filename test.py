import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import quote
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def sliced(headlines):
    publishers = ["CNN", "Fox", "Politico", "NBC News", "The New York Times", "BBC", "The Economist", "The Washington Post", "WSJDUBAI", "Literary Hub"]
    sliced_headlines = []
    for headline in headlines:
        for publisher in publishers:
            if publisher in headline:
                publisher_index = headline.find(publisher)
                sliced_headline = headline[:publisher_index].strip()
                sliced_headlines.append(sliced_headline)
                break
        else:
            sliced_headlines.append(headline)
    return sliced_headlines

def remove_short_headlines(headlines):
    """
    Remove headlines with less than 3 words from the headlines list.
    
    Args:
        headlines (list): List of headlines.
    
    Returns:
        list: Filtered list of headlines.
    """
    filtered_headlines = [headline for headline in headlines if len(headline.split()) >= 5]
    return filtered_headlines

def remove_ellipsis(headlines):
    """
    Remove ellipsis (...) and everything after it from headlines.
    
    Args:
        headlines (list): List of headlines.
    
    Returns:
        list: List of headlines with ellipsis removed.
    """
    cleaned_headlines = []
    for headline in headlines:
        if "..." in headline:
            # Find the index of "..." and slice the headline
            ellipsis_index = headline.find("...")
            cleaned_headline = headline[:ellipsis_index]
            cleaned_headlines.append(cleaned_headline.strip())  # Strip to remove leading/trailing whitespace
        elif "." in headline:
            # Find the index of "..." and slice the headline
            ellipsis_index = headline.find(".")
            cleaned_headline = headline[:ellipsis_index]
            cleaned_headlines.append(cleaned_headline.strip())  # Strip to remove leading/trailing whitespace
        elif "·" in headline:
            # Find the index of "..." and slice the headline
            ellipsis_index = headline.find("·")
            cleaned_headline = headline[:ellipsis_index]
            cleaned_headlines.append(cleaned_headline.strip())  # Strip to remove leading/trailing whitespace
        else:
            cleaned_headlines.append(headline)
    return cleaned_headlines

def get_google_news_headlines(topic):
    url = f"https://www.google.com/search?q={topic}&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors
    
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    # Adjusted CSS selector to match the headline class
    button_elements = soup.find_all('a')
    for button in button_elements:
        headlines.append(button.get_text())
    headlines = remove_short_headlines(headlines)
    headlines = remove_ellipsis(headlines)
    headlines = sliced(headlines)
    return headlines  # Limit to the top 100 headlines

    

if __name__ == "__main__":
    topic = input("Enter the topic: ")
    headlines = get_google_news_headlines(topic)
    if headlines:
        print("Top 100 headlines on Google News for", topic, ":")
        for i, headline in enumerate(headlines, start=1):
            print(f"{i}. {headline}")
    else:
        print("No headlines found for the given topic.")