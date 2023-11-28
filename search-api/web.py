import asyncio
from json import dumps
from flask import Flask, Response, request, jsonify
from scraper import search, images
from os import getenv
from dotenv import load_dotenv

PORT = 3000

loop = asyncio.new_event_loop()
app = Flask("FitGPT Search API")
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True # pretty json

@app.route("/")
def index():
    return Response("Hello CS 416", 200)

@app.route("/youtube")
def search_title():
    q = request.args.get("query", None) or request.args.get("q", None) or request.args.get("title", None)
    filter_ = request.args.get("filter", None)

    if q == None:
        return Response("No query provided", 400)
    else:
        res = loop.run_until_complete(search(q, filter_))
        return jsonify(res)
    
@app.route("/images")
def google_images():
    q = request.args.get("q", None)

    if q == None:
        return Response("No query provided", 400)
    else:
        res = images(q)
        return jsonify(res)

app.run("127.0.0.1", PORT)