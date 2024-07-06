import requests
from bs4 import BeautifulSoup
import pyshorteners
# URL shortening function
def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

def scrape_news_itatiaia(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_data = []
    
    for item in soup.select('div.PagePromo-title a.Link'):
        title = item.get_text(strip=True) #Texto sem espaços em branco
        href = item['href'] ##Pega o links
        news_data.append((title, href))

    return news_data

def scrape_news_estado_de_minas(url):
    position = url.find('.br') + 3  # +3 to include '.br'
    cropped_url = url[:position]

    response = requests.get(url)
    if response.encoding is None or response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.content, 'html.parser')
    news_links = soup.find_all('a', class_='jumbotron-default-link')

    news_data = []
    for link in news_links:
        title = link.get('title')
        href = link.get('href')
        if href and href.startswith('/'):
            href = cropped_url + href
        news_data.append((title, href))
    return news_data

def scrape_news_o_tempo(url):
    position = url.find('.br') + 3  # +3 to include '.br'
    cropped_url = url[:position]

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_data = []
    
    for item in soup.find_all('h2', class_='list__description'):
        title = item.get_text(strip=True) #Texto sem espaços em branco
        parent = item.find_parent('a') #Como eu utilizei o h2, eu preciso voltar um nível para pegar o link
        href = parent['href'] 
        if href and href.startswith('/'):
            href = cropped_url + href
        news_data.append((title, href))

    return news_data

def gather_news_EM(news_sources):
    all_news = {}
    for url, category in news_sources.items():
        news = scrape_news_estado_de_minas(url)
        if category not in all_news:
            all_news[category] = []
        all_news[category].extend(news)

    return all_news

def gather_news_itatiaia(all_news, k):
    politica_url = 'https://www.itatiaia.com.br/politica'  
    economia_url = 'https://www.itatiaia.com.br/economia'  
    
    politica_news = scrape_news_itatiaia(politica_url)[:k]
    economia_news = scrape_news_itatiaia(economia_url)[:k]

    all_news['política'] = politica_news
    all_news['economia'] = economia_news

def gather_news_o_tempo(all_news, k):
    politica_url = 'https://www.otempo.com.br/politica'  
    economia_url = 'https://www.otempo.com.br/economia'  
    
    politica_news = scrape_news_o_tempo(politica_url)[:k]

    economia_news = scrape_news_o_tempo(economia_url)[:k]

    all_news['política'] = politica_news
    all_news['economia'] = economia_news

def format_news(all_news):
    news_text = ""
    for category, items in all_news.items():
        news_text += f"📌 {category.title()}:\n"
        for title, link in items:
            short_link = shorten_url(link)
            news_text += f"📰 {title}: {short_link}\n"
        news_text += "\n"

    return news_text

if __name__ == "__main__":
    #Não vi necessidade de importar essas bibliotecas, entao comentei
    #from datetime import datetime
    #from tqdm import tqdm 

    #O número de noticias que o usuário só funcionam para o Itatiaia e o O Tempo,
    #pois o código do EM já foi previamente fornecido e eu não quis mexer nele
    k = int(input("Quantas notícias deseja ver de cada tópico deseja ver? "))

    # News websites and categories for Estado de Minas
    news_sources_EM = {
        'https://www.em.com.br/politica/': 'Política',
        'https://www.em.com.br/economia/': 'Economia',
        'https://www.em.com.br/educacao/': 'Educação',
    }   

    #------------------------Recebimento de notícias de Estado de Minas 
    all_news_EM = gather_news_EM(news_sources_EM)
    news_text_EM = format_news(all_news_EM)

    print("Estado de Minas News:")
    print(news_text_EM)

    #------------------------Recebimento de notícias de Itatiaia 
    all_news_itatiaia = {}

    gather_news_itatiaia(all_news_itatiaia, k)
    news_text_itatiaia = format_news(all_news_itatiaia)

    print("Itatiaia News:")
    print(news_text_itatiaia)

    #------------------------Recebimento de notícias de O Tempo
    all_news_o_tempo = {}

    gather_news_o_tempo(all_news_o_tempo, k)
    news_text_o_tempo = format_news(all_news_o_tempo)
    
    print("O Tempo News:")
    print(news_text_o_tempo)