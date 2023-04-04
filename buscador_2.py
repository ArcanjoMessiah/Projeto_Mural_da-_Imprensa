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
    # Cria o arquivo HTML com as manchetes em cards do Bootstrap 5
    with open("headlines.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("<head>\n")
        f.write("<meta charset='utf-8'>\n")
        f.write("<meta name='viewport' content='width=device-width, initial-scale=1'>\n")
        f.write("<title>Principais Manchetes</title>\n")
        f.write("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.0.2/css/bootstrap.min.css'>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<div class='container mt-3'>\n")
        f.write("<h1 class='mb-3'>Principais Manchetes</h1>\n")
        f.write("<div class='mb-3'>\n")
        f.write("<label for='categoryFilter' class='form-label'>Filtrar por Categoria:</label>\n")
        f.write("<select id='categoryFilter' class='form-select'>\n")
        f.write("<option value=''>Todas</option>\n")
