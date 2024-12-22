import requests

import json

URL_QUINTO_ANDAR = (
    "https://apigw.prod.quintoandar.com.br/cached/house-listing-search/v2/search/list"
)


def montar_resposta_casa(dados_casa):
    return {
        "_id": dados_casa["_id"],
        "address": dados_casa["_source"]["address"],
        "neighbourhood": dados_casa["_source"]["neighbourhood"],
        "regionName": dados_casa["_source"]["regionName"],
        "type": dados_casa["_source"]["type"],
        "area": dados_casa["_source"]["area"],
        "bathrooms": dados_casa["_source"]["bathrooms"],
        "bedrooms": dados_casa["_source"]["bedrooms"],
        "totalCost": dados_casa["_source"]["totalCost"],
        "iptuPlusCondominium": dados_casa["_source"]["iptuPlusCondominium"],
    }


def tratar_resposta(json_5andar_response):
    houses = json_5andar_response["hits"]
    return [montar_resposta_casa(dados_casa) for dados_casa in houses]


def montar_requisicao(bu_context, bairro_jdi, qtd_paginacao):
    return {
        "context": {"mapShowing": True, "listShowing": True, "userId": 0},
        "filters": {
            "businessContext": bu_context,
            "blocklist": [],
            "selectedHouses": [],
            "location": {
                "coordinate": bairro_jdi["coords"],
                "neighborhoods": [],
                "countryCode": "BR",
            },
            "priceRange": [],
            "specialConditions": [],
            "excludedSpecialConditions": [],
            "houseSpecs": {
                "area": {"range": {}},
                "houseTypes": [],
                "amenities": [],
                "installations": [],
                "bathrooms": {"range": {}},
                "bedrooms": {"range": {}},
                "parkingSpace": {"range": {}},
                "suites": {"range": {}},
            },
            "availability": "ANY",
            "occupancy": "ANY",
            "partnerIds": [],
            "categories": [],
        },
        "sorting": {"criteria": "RELEVANCE", "order": "DESC"},
        "pagination": {"pageSize": qtd_paginacao, "offset": 0},
        "slug": bairro_jdi["slug"],
        "fields": [
            "id",
            "rent",
            "totalCost",
            "salePrice",
            "iptuPlusCondominium",
            "area",
            "address",
            "regionName",
            "city",
            "type",
            "forRent",
            "neighbourhood",
            "categories",
            "bathrooms",
            "bedrooms",
        ],
        "locationDescriptions": [{"description": bairro_jdi["slug"]}],
    }


bairros_jdi = [
    {
        "slug": "vila-progresso-jundiai-sp-brasil",
        "coords": {"lat": -23.217214, "lng": -46.864882},
    },
    {
        "slug": "malota-jundiai-sp-brasil",
        "coords": {"lat": -23.2104496, "lng": -46.9288827},
    },
    {
        "slug": "jundiai-aglomeracao-urbana-de-jundiai-jundiai-sp-brasil",
        "coords": {"lat": -23.1856528, "lng": -46.8892222},
    },
]


for bairro_jdi in bairros_jdi:
    payload = montar_requisicao("RENT", bairro_jdi, 100)
    response_5a = requests.post(URL_QUINTO_ANDAR, json=payload)

    if response_5a.status_code < 400:
        json_resp_5a = response_5a.json()

        casas = tratar_resposta(json_resp_5a["hits"])

        with open(f"temp/{bairro_jdi["slug"]}.json", "w") as json_file:
            casas_json = json.dumps(casas)

            json_file.write(casas_json)

    else:
        print(response_5a.json())
