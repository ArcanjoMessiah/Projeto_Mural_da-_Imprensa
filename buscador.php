<?php

// Lista de sites para verificar as manchetes
$sites = [
    ['url' => 'https://g1.globo.com/', 'source' => 'G1'],
    ['url' => 'https://www.correiobraziliense.com.br/', 'source' => 'Correio Braziliense'],
    ['url' => 'https://www.estadao.com.br/', 'source' => 'Estadão'],
    ['url' => 'https://oglobo.globo.com/', 'source' => 'O Globo'],
    ['url' => 'https://www.jornaldacidadeonline.com.br/', 'source' => 'Jornal da Cidade Online']
];

// Dicionário de temas para filtro
$temas = [
    'politica' => 'Política',
    'esportes' => 'Esportes',
    'economia' => 'Economia',
    'moda' => 'Moda',
    'tecnologia' => 'Tecnologia',
    'cultura' => 'Cultura',
    'saude' => 'Saúde',
    'ultimas' => 'Últimas Notícias',
    'internacionais' => 'Internacionais'
];

// Definição do intervalo em segundos
$intervalo = 1800;  // 30 minutos 

// Função para obter as manchetes de um site
function get_headlines($site) {
    $html = file_get_contents($site['url']);
    $doc = new DOMDocument();
    @$doc->loadHTML($html);
    $links = $doc->getElementsByTagName('a');
    $headlines = array();
    foreach ($links as $link) {
        $text = trim($link->nodeValue);
        $href = trim($link->getAttribute('href'));
        if ($text !== "" && $href !== "") {
            $headline = array(
                'title' => $text,
                'link' => $href,
                'source' => $site['source'],
                'image' => '',
                'summary' => ''
            );
            array_push($headlines, $headline);
        }
    }
    return $headlines;
}


// Função para atualizar as manchetes
function update_headlines() {
    while (true) {
        // Obtém as manchetes de cada site
        $all_headlines = array();
        foreach ($GLOBALS['sites'] as $site) {
            $all_headlines[$site['source']] = get_headlines($site);
        }

        // Adiciona o resumo de cada manchete
        foreach ($all_headlines as $source => &$headlines_site) {
            foreach ($headlines_site as &$headline) {
                $html = file_get_contents($headline['link']);
                $doc = new DOMDocument();
                @$doc->loadHTML($html);
                $meta = $doc->getElementsByTagName('meta');
                foreach ($meta as $tag) {
                    if ($tag->getAttribute('name') == 'description') {
                        $headline['summary'] = $tag->getAttribute('content');
                        break;
                    }
                }
            }
        }
        
       


        // Cria o conteúdo HTML com as manchetes e temas
        $html_content = '';
        foreach ($GLOBALS['temas'] as $tema => $tema_nome) {
            $html_content .= '<h2>' . $tema_nome . '</h2>';
            $html_content .= '<div class="card-columns">';
            foreach ($all_headlines as $source => $headlines_site) {
                foreach ($headlines_site as $headline) {
                    // Verifica se a manchete pertence ao tema
                    if (strpos(strtolower($headline['title']), strtolower($tema_nome)) !== false) {
                        $html_content .= '<div class="card bg-secondary">';
                        $html_content .= '<div class="card-body">';
                        $html_content .= '<h5 class="card-title">' . $headline['title'] . '</h5>';
                        $html_content .= '<p class="card-text">' . $headline['summary'] . '</p>';
                        $html_content .= '<a href="' . $headline['link'] . '" class="card-link">' . $source . '</a>';
                        $html_content .= '</div>';
                        $html_content .= '</div>';
                    }
                }
            }
            $html_content .= '</div>';
        }

         // Imprime o tempo atual
         echo "Atualizado em " . date('H:i:s') . "\n";
        
         // Espera 30 minutos antes de executar novamente
         sleep(1800);
     

    }

}



    ?>
