import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
import time

# Lista de sites para verificar as manchetes
sites = [
    {'url': 'https://g1.globo.com/', 'source': 'G1'},
    {'url': 'https://www.correiobraziliense.com.br/', 'source': 'Correio Braziliense'},
    {'url': 'https://www.estadao.com.br/', 'source': 'Estadão'},
    {'url': 'https://oglobo.globo.com/', 'source': 'O Globo'},
    {'url': 'https://www.jornaldacidadeonline.com.br/', 'source': 'Jornal da Cidade Online'}
]

# Dicionário de temas para filtro
temas = {
    'politica': 'Política',
    'esportes': 'Esportes',
    'economia': 'Economia',
    'moda': 'Moda',
    'tecnologia': 'Tecnologia',
    'cultura': 'Cultura',
    'saude': 'Saúde',
    'ultimas': 'Últimas Notícias',
    'internacionais': 'Internacionais'
}

# Definição do intervalo em segundos
intervalo = 1800  # 30 minutos

# Função para obter as manchetes de um site
def get_headlines(site):
    r = requests.get(site['url'])
    soup = BeautifulSoup(r.content, 'html.parser')
    headlines = []
    for headline in soup.find_all('a'):
        if headline.get('href') and headline.text:
            headline_dict = {
                'title': headline.text,
                'link': headline.get('href'),
                'source': site['source'],
                'image': '',
                'summary': ''
            }
            headlines.append(headline_dict)
    return headlines

# Função para atualizar as manchetes
def update_headlines():
    while True:
        # Obtém as manchetes de cada site
        all_headlines = {}
        for site in sites:
            all_headlines[site['source']] = get_headlines(site)

        # Adiciona o resumo de cada manchete
        for source, headlines_site in all_headlines.items():
            for headline in headlines_site:
                try:
                    r = requests.get(headline['link'])
                    soup = BeautifulSoup(r.content, 'html.parser')
                    headline['summary'] = soup.find('meta', attrs={'name': 'description'})['content']
                except:
                    pass

        # Cria o conteúdo HTML com as manchetes e temas
        html_content = ''
        for tema in temas:
            html_content += '<h2>' + temas[tema] + '</h2>'
            html_content += '<ul class="list-group">'
            for source, headlines_site in all_headlines.items():
                for headline in headlines_site:
                    if tema.lower() in headline['title'].lower():
                        html_content += '<li class="list-group-item"><a href="' + headline['link'] + '">' + headline['title'] + '</a></li>'
            html_content += '</ul>'

        # Atualiza o arquivo HTML com o conteúdo gerado dinamicamente
        with open('templates/manchetes.html', 'w') as f:
            f.write(html_content)

        print('Arquivo HTML atualizado com sucesso.')

        time.sleep(intervalo)

app = Flask(__name__)

# Rota principal para exibição das manchetes
@app.route('/')
def index():
    # Retorna o conteúdo HTML gerado pela função update_headlines()
    return render_template('manchetes.html', noticias=sites)

if __name__ == '__main__':
    app.run()
