import requests
from bs4 import BeautifulSoup
import time
import os

# URL dos sites que serão verificados
urls = [
    "https://g1.globo.com/",
    "https://www.correiobraziliense.com.br/",
    "https://www.estadao.com.br/",
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
    response = requests.get(url, timeout=10)
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


# Loop principal para verificar as manchetes a cada 30 minutos
while True:
    all_headlines = []
    for url in urls:
        try:
            all_headlines += get_headlines(url)
        except requests.exceptions.Timeout:
            print("Timeout ao acessar:", url)
        except Exception as e:
            print("Erro ao acessar", url, ":", str(e))
    # Ordena as manchetes por categoria
    sorted_headlines = {}
    for category in categories.keys():
        sorted_headlines[category] = []
        for headline in all_headlines:
            if headline["category"] == category:
                sorted_headlines[category].append(headline)
    # Imprime as manchetes em HTML com cards do Bootstrap 5
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Notícias do dia</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
    """
    for category in sorted_headlines.keys():
        if sorted_headlines[category]:
            html += f"<h2>{category.capitalize()}</h2>"
            html += "<div class='row row-cols-1 row-cols-md-3 g-4'>"
            for headline in sorted_headlines[category]:
                html += "<div class='col'>"
                html += "<div class='card h-100'>"
                html += "<div class='card-body'>"
                html += f"<h5 class='card-title'>{headline['title']}</h5>"
                html += f"<a href='{headline['link']}' class='btn btn-primary'>Ler mais</a>"
                html += "</div></div></div>"
                html += "</div>"
    # Salva o resultado em um arquivo HTML
    html_file_path = "D:\laragon\www\Projeto_Mural_da_imprensa\manchetes.html"

    with open(html_file_path, "w") as file:
        file.write(html)


# Aguarda 30 minutos antes de verificar novamente
    time.sleep(6000)

