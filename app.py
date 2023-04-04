from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Lista de sites para verificar as manchetes
sites = [
    'https://g1.globo.com/',
    'https://www.correiobraziliense.com.br/',
    'https://www.estadao.com.br/',
    'https://oglobo.globo.com/',
    'https://www.jornaldacidadeonline.com.br/'
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
    r = requests.get(site)
    soup = BeautifulSoup(r.content, 'html.parser')
    headlines = []
    for headline in soup.find_all('a'):
        if headline.get('href') and headline.text:
            img = None
            img_tag = headline.find_previous('img')
            if img_tag:
                img = img_tag.get('src')
            headlines.append({
                'title': headline.text,
                'link': headline.get('href'),
                'img': img
            })
    return headlines

# Rotas
@app.route('/')
def index():
    # Obtém as manchetes de cada site
    all_headlines = {}
    for site in sites:
        all_headlines[site] = get_headlines(site)
    
    return render_template('index.html', all_headlines=all_headlines, temas=temas)

@app.route('/tema/<tema>')
def tema(tema):
    # Obtém as manchetes filtradas pelo tema especificado
    tema_headlines = {}
    for site in sites:
        all_headlines = get_headlines(site)
        tema_headlines[site] = [h for h in all_headlines if tema.lower() in h['title'].lower()]
    
    return render_template('tema.html', tema_headlines=tema_headlines, tema=temas[tema])

if __name__ == '__main__':
    app.run(debug=True)
