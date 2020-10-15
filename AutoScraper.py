import json

from autoscraper import AutoScraper
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


def get_pagina_result(url, link):
    PAGINA_scraper = AutoScraper()
    PAGINA_scraper.load('./' + url + '-search.json')
    result = PAGINA_scraper.get_result_similar(link,unique=True, group_by_alias=True)
    return _aggregate_result(result)


def _aggregate_result(result):
    final_result = []

    #new_dict = {a: list(set(b)) for a, b in result.items()}
    for i in range(len(list(result.values())[0])):
        try:
            final_result.append({alias: result[alias][i] for alias in result})
        except IndexError:
            pass
        continue
    return final_result

@app.route('/GuardarRegla', methods=['POST'])
def autoscraper():
    regla = request.json["regla"]
    scraper.keep_rules(regla)
    pagina = url.replace("http:", "").replace("//", "").replace(".", "").replace("www", "").replace(
        "https:", "").replace("/", "").replace("\n", "").replace("-", "")

    scraper.save(pagina + '-search.json')


@app.route('/ObtenerRegla', methods=['POST'])
def autoscraper():
    link = request.json["Link"]
    global url
    url = request.json["Link"]
    wanted_list = request.json["Metodo"]
    global scraper
    scraper = AutoScraper()
    wanted_dict = {
        'url': ['https://www.rosario3.com/policiales/Robaron-dos-autos-de-alta-gama-de-una-concesionaria-y-los-encontraron-en-un-galpon-20201014-0080.html',
                'https://www.rosario3.com/-economia-negocios-agro-/La-inflacion-de-septiembre-fue-del-28-segun-el-Indec-20201014-0087.html',
                'https://www.rosario3.com/informaciongeneral/Coronavirus-confirmaron-el-primer-caso-de-reinfeccion-en-Rosario-20201014-0030.html']
    }
    scraper.build(url=link, wanted_dict=wanted_dict)
    dict = scraper.get_result_similar(link, grouped=True)

    regla = []
    [regla.extend([k]) for k in dict.keys()]
    #data = get_pagina_result(url, link)
    #json_format = json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
    return regla


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/rosario3', methods=['GET'])
def search_api():
    return dict(result=get_pagina_result())


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
