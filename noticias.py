import requests
from bs4 import BeautifulSoup
import time
import json

# Lista de sites para verificar as manchetes
sites = [
    {'url': 'https://g1.globo.com/', 'source': 'G1'},
    {'url': 'https://www.correiobraziliense.com.br/', 'source': 'Correio Braziliense'},
    {'url': 'https://www.estadao.com.br/', 'source': 'Estadão'},
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

# Função para atualizar o arquivo JSON
def update_json():
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

    # Cria o dicionário com as manchetes e temas
    data = {}
    for tema in temas:
        headlines = []
        for source, headlines_site in all_headlines.items():
            headlines += [h for h in headlines_site if tema.lower() in h['title'].lower()]
        data[temas[tema]] = headlines

    # Salva o arquivo JSON
    with open('manchetes.json', 'w') as f:
        json.dump(data, f)

    print('Arquivo JSON atualizado com sucesso.')

# Define o intervalo de tempo para atualizar o arquivo JSON (em segundos)
intervalo = 3600

while True:
    update_json()
    time.sleep(intervalo)
