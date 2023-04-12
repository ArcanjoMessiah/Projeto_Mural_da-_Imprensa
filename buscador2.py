import time
import requests
from bs4 import BeautifulSoup


urls = [
    "https://g1.globo.com/",
    "https://www.correiobraziliense.com.br/",
    "https://www.estadao.com.br/",
    "https://www.jornaldacidadeonline.com.br/"
]
timeout = 5
sorted_headlines = {}

for url in urls:
    try:
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all('h3')[:6]
        category = url.split('.')[1]
        sorted_headlines[category] = []
        for headline in headlines:
            sorted_headlines[category].append({'title': headline.text, 'link': url})
    except:
        continue
    
while True:
    html = ""
    for url in urls:
        try:
            response = requests.get(url, timeout=timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = soup.find_all('h3')[:6]
            category = url.split('.')[1]
            if category not in sorted_headlines:
                sorted_headlines[category] = []

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
            for headline in headlines:
                if any(headline['title'] == h['title'] for h in sorted_headlines[category]):
                    continue
                sorted_headlines[category].append({'title': headline.text, 'link': url})
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
        except:
            continue
     # Salva o resultado em um arquivo HTML
    html_file_path = "D:\laragon\www\Projeto_Mural_da_imprensa\manchetes.html"

    with open(html_file_path, "w") as file:
        file.write(html)

    time.sleep(6000)