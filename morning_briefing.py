import requests
from bs4 import BeautifulSoup
import pyshorteners

# URL shortening function
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

def scrape_news_itatiaia(url):
    pass

def scrape_news_o_tempo(url):
    pass

def scrape_news_estado_de_minas(url):
    position = url.find('.br') + 3  # +3 to include '.br'
    cropped_url = url[:position]

    # Send a GET request to the website
    response = requests.get(url)
    # Ensure the correct encoding is used based on the webpage's content type
    if response.encoding is None or response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')  # Use response.content to avoid re-encoding issues
    # Find all <a> elements with the class 'jumbotron-default-link'
    news_links = soup.find_all('a', class_='jumbotron-default-link')
    # Prepare a list to store tuples of (title, link)
    news_data = []
    for link in news_links:
        title = link.get('title')  # Extract the title from the 'title' attribute
        href = link.get('href')  # Extract the URL from the 'href' attribute
        # Check if the link is relative and prepend the base URL if needed
        if href and href.startswith('/'):
            href = cropped_url + href  # Append the base domain to the relative URL
        # Append the tuple (title, href) to the list
        news_data.append((title, href))
    return news_data

def gather_news_o_tempo(news_sources):
    pass

def gather_news_itatiaia(url):
    pass

def gather_news_EM(news_sources):
        # Gather all news
    all_news = {}
    for url, category in news_sources.items():
        news = scrape_news_estado_de_minas(url)
        if category not in all_news:
            all_news[category] = []
        all_news[category].extend(news)

    return all_news

def format_news(all_news):
    # Format news text
    news_text = ""
    for category, items in all_news.items():
        news_text += f"📌 {category.title()}:\n"
        for title, link in items:
            short_link = shorten_url(link)
            news_text += f"📰 {title}: {short_link}\n"
        news_text += "\n"

    return news_text

    

if __name__ == "__main__":

    from datetime import datetime
    from tqdm import tqdm
   
    # News websites and categories (example)
    news_sources_EM = {
        'https://www.em.com.br/politica/': 'Política',
        'https://www.em.com.br/economia/': 'Economia',
        'https://www.em.com.br/educacao/': 'Educação',
        # Add more sources as needed
    }

    all_news = gather_news_EM(news_sources_EM)
    news_text = format_news(all_news)
    print(news_text)



    
