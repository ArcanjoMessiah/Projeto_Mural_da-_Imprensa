<?php
include_once "complement.html";

?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Notícias</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" integrity="sha384-Zf0v1jAr+Ra8q2dOTU6fOPh6OdD0WlyoyKX9G0N5d5O5KjF5ue5InPgNFegexzY5" crossorigin="anonymous">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Notícias</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    {% for tema in temas %}
                    <li class="nav-item">
                        <a class="nav-link" href="/tema/{{ tema }}">{{ temas[tema] }}</a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container my-4">
        <div class="row row-cols-1 row-cols-md-3 g-4">
            {% for site in all_headlines %}
            {% for headline in all_headlines[site] %}
            <div class="col">
                <div class="card">
                    {% if headline.image %}
                    <img src="{{ headline.image }}" class="card-img-top" alt="...">
                    {% endif %}
                    <div class="card-body">
                        <h5 class="card-title">{{ headline.title }}</h5>
                        <p class="card-text">{{ headline.summary }}</p>
                        <a href="{{ headline.link }}" class="btn btn-primary">Ler mais</a>
                    </div>
                </div>
            </div>
            {% endfor %}
            {% endfor %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-U0Nvq3iXFeJrGzSwLxowkKd/iJp7GwRraHo8W7b/XnJ5Y5X5cx5+kOk8CfZ/Cdm" crossorigin="anonymous"></script>
</body>
</html>