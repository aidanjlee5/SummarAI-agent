# Methods used for fetching data and inserting data into the database

"""def get_data(db):
    results = []
    topic = db.table('summarizations').select('topic').execute()
    headline = db.table('summarizations').select('headline').execute()
    summarization = db.table('summarizations').select('summarization').execute()
    results = [topic, headline, summarization]
    return results"""

def insert_data(db, headline, summarization, topic, url):
    db.table('summarizations').insert([{
        'headline': headline,
        'summarization': summarization,
        'topic': topic,
        'url': url,
    }]).execute()
    