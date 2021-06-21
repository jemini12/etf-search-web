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
def dashboard():
    useragent = request.user_agent.string
    app.logger.info("user request for /dashboard " + useragent)
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
            "includes": ["etfName", "etfProfits", "etfTypes.etfType"]
        }
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
            }
        }
        headers = {'Content-Type': 'application/json'}
        rtn = requests.get(
            app.config['ES_URL'] + "etf-search-latest/_search", json=query, headers=headers)
        etflist = rtn.json()['hits']['hits']
        return render_template('index/result.html', etflist=etflist, keyword=keyword, is_mobile=is_mobile)

    except Exception as e:
        app.logger.info(e)
        return make_response("Internal Error", 500)
