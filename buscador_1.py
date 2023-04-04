import requests
from bs4 import BeautifulSoup
import time

# URL dos sites que serão verificados
urls = [
    "https://g1.globo.com/",
    "https://www.correiobraziliense.com.br/",
    "https://www.estadao.com.br/",
    "https://oglobo.globo.com/",
    "https://www.jornaldacidadeonline.com.br/"
]

# Dicionário para mapear as categorias das notícias
categories = {
    "politics": ["política"],
    "sports": ["esporte"],
    "economy": ["economia"],
    "fashion": ["moda"],
    "technology": ["tecnologia", "ciência"],
    "culture": ["cultura", "entretenimento"],
    "health": ["saúde", "bem-estar"],
    "latest_news": ["últimas notícias"],
    "international": ["internacional"]
}

# Função para extrair as manchetes de uma página
def get_headlines(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = []
    for headline in soup.find_all("a", class_="feed-post-link"):
        title = headline.text.strip()
        link = headline["href"]
        category = ""
        for key, values in categories.items():
            for value in values:
                if value in title.lower():
                    category = key
                    break
            if category:
                break
        headlines.append({"title": title, "link": link, "category": category})
    return headlines

# Loop principal para verificar as manchetes a cada hora
while True:
    all_headlines = []
    for url in urls:
        all_headlines += get_headlines(url)
    # Ordena as manchetes por categoria
    sorted_headlines = {}
    for category in categories.keys():
        sorted_headlines[category] = []
        for headline in all_headlines:
            if headline["category"] == category:
                sorted_headlines[category].append(headline)
    # Imprime as manchetes em HTML com cards do Bootstrap 4
    html = "<div class='container'>"
    for category in sorted_headlines.keys():
        if sorted_headlines[category]:
            html += "<h2>" + category.capitalize() + "</h2>"
            html += "<div class='row'>"
            for headline in sorted_headlines[category]:
                html += "<div class='col-md-4'>"
                html += "<div class='card mb-4 shadow-sm'>"
                html += "<div class='card-body'>"
                html += "<h5 class='card-title'>" + headline["title"] + "</h5>"
                html += "<a href='" + headline["link"] + "' class='btn btn-primary'>Ler mais</a>"
                html += "</div></div></div>"
            html += "</div>"
    html += "</div>"
    # Salva o resultado em um arquivo HTML