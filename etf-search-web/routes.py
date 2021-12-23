from flask.helpers import make_response
import requests
import json

from flask import (
    Blueprint, render_template, request, jsonify, send_from_directory, current_app as app
)
from werkzeug.wrappers import response
bp = Blueprint('index', __name__)


@bp.route("/")
def index():
    useragent = request.user_agent.string
    app.logger.info("user request for / " + useragent)
    if "mobile" in useragent.lower():
        is_mobile = True
    else:
        is_mobile = False
    query = {
        "size": 1000,
        "query": {
            "match_all": {}
        },
        "_source": {
            "includes": ["etfName", "etfProfits"]
        }
    }
    headers = {'Content-Type': 'application/json'}
    rtn = requests.get(
        app.config['ES_URL'] + "etf-search-latest/_search", json=query, headers=headers)
    etflist = rtn.json()['hits']['hits']

    return render_template('index/index.html', etflist=etflist, is_mobile=is_mobile)


@bp.route("/etflist")
def etflist():
    useragent = request.user_agent.string
    app.logger.info("user request for /etflist " + useragent)
    if "mobile" in useragent.lower():
        is_mobile = True
    else:
        is_mobile = False
    query = {
        "size": 1000,
        "query": {
            "match_all": {}
        },
        "_source": {
            "excludes": ["etfDescription", "etfElements"]
        },
        "fields": ["perAvg", "roeAvg", "pbrAvg"]
    }
    headers = {'Content-Type': 'application/json'}
    rtn = requests.get(
        app.config['ES_URL'] + "etf-search-latest/_search", json=query, headers=headers)
    etflist = rtn.json()['hits']['hits']
    return render_template('etflist/etflist.html', etflist=etflist, is_mobile=is_mobile)


@bp.route("/sitemap.xml")
@bp.route("/robots.txt")
def robot():
    return send_from_directory(app.static_folder, request.path[1:])


@bp.route("/autocomplete/<keyword>", methods=['GET'])
def autocomplete(keyword):
    app.logger.info(f"frontend request for /autocomplete/{keyword} ")
    try:
        query = {
            "size": 10,
            "query": {
                "bool": {
                "filter": [
                    {
                    "wildcard": {
                        "stockName": {
                        "value": f"{keyword}*",
                        "case_insensitive": "true"
                        }
                    }
                    }
                ]
                }
            },
            "_source": {
                "includes": [
                "stockName"
                ]
            },
            "sort": [
                {
                "code": {
                    "order": "asc"
                }
                }
            ]
        }
        headers = {'Content-Type': 'application/json'}
        rtn = requests.get(
            app.config['ES_URL'] + "stock-data-latest/_search", json=query, headers=headers)
        stocklist = rtn.json()['hits']['hits']
        autocompleteList = []
        for stock in stocklist:
            autocompleteList.append(stock['_source']['stockName'])
            
        return make_response(json.dumps(autocompleteList, ensure_ascii=False), 200)
    except Exception as e:
        app.logger.info(e)
        return make_response("Internal Error", 500)


@bp.route("/search/<keyword>", methods=['GET'])
def search(keyword):
    useragent = request.user_agent.string
    app.logger.info(f"user request for /search/{keyword} " + useragent)
    if "mobile" in useragent.lower():
        is_mobile = True
    else:
        is_mobile = False
    try:
        query = {
            "size": 100,
            "query": {
                "nested": {
                    "path": "etfElements",
                    "inner_hits": {
                        "_source": [
                            "etfElements.stockName",
                            "etfElements.stockPortion"
                        ]
                    },
                    "query": {
                        "bool": {
                            "filter": [
                                {
                                    "term": {
                                        "etfElements.stockName.keyword": keyword
                                    }
                                },
                                {
                                    "exists": {
                                        "field": "etfElements.stockPortion"
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            "_source": {
                "includes": [
                    "etfName",
                    "etfProfits"
                ]
            },
            "fields": ["perAvg", "roeAvg", "pbrAvg"]
        }
        headers = {'Content-Type': 'application/json'}
        rtn = requests.get(
            app.config['ES_URL'] + "etf-search-latest/_search", json=query, headers=headers)
        etflist = rtn.json()['hits']['hits']
        return render_template('index/result.html', etflist=etflist, keyword=keyword, is_mobile=is_mobile)

    except Exception as e:
        app.logger.info(e)
        return make_response("Internal Error", 500)
