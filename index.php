<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Notícias</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css">
</head>

<body>
    <div class="container mt-5">
        <h1 class="mb-5">Notícias</h1>

        <div class="row row-cols-1 row-cols-md-3 g-4">
            <?php
            // lê o arquivo json e armazena em um array associativo
            $noticias = json_decode(file_get_contents('manchetes.json'), true);

            // itera pelas manchetes de cada site
            foreach ($noticias as $site => $manchetes) {
                echo '<div class="col">';
                echo '<div class="card h-100">';
                echo '<div class="card-body">';
                echo '<h2 class="card-title">' . $site . '</h2>';
                echo '<ul class="list-group list-group-flush">';

                // itera pelas manchetes do site atual
                foreach ($manchetes as $manchete) {
                    echo '<li class="list-group-item">';
                    echo '<a href="' . $manchete['link'] . '">' . $manchete['title'] . '</a>';

                    // se houver imagem, exibe-a
                    if (isset($manchete['image'])) {
                        echo '<div class="my-3">';
                        echo '<img src="' . $manchete['image'] . '" class="card-img-top img-fluid" alt="Imagem da notícia">';
                        echo '</div>';
                    }

                    echo '<p class="card-text">' . $manchete['resumo'] . '</p>';
                    echo '</li>';
                }

                echo '</ul>';
                echo '</div>';
                echo '</div>';
                echo '</div>';
            }
            ?>
        </div>

    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"></script>

    <pre>
<?php print_r($noticias); ?>
</pre>
</body>

</html>
