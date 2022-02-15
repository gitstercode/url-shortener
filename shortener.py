#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, jsonify
import pyshorteners as pyshorteners
from pyshorteners.exceptions import BadAPIResponseException, BadURLException, ShorteningErrorException, ExpandingErrorException

app = Flask(__name__)
ACCESS_TOKEN = '043cf734af9d8f4e0891bc079fb8b34957141500'

@app.route('/shortify',strict_slashes=False, methods=['GET'])
def shortify():
    url = request.args.get('url')
    if not url:
        return {'error': 'param url is mandatory'},400

    try:
        url_shortener = pyshorteners.Shortener(api_key=ACCESS_TOKEN) 
        clean_url = url_shortener.bitly.clean_url(url)
        short_url = url_shortener.bitly.short(clean_url)
        response = jsonify({'short_url': short_url}), 200
    except (ShorteningErrorException, BadURLException, BadAPIResponseException, Exception ) as e:
        response = {'error': [e.args] }, 500

    return response

@app.route('/longify',strict_slashes=False, methods=['GET'])
def longify():
    url = request.args.get('url')
    if not url:
        return {'error': 'param url is mandatory'},400

    try:
        url_shortener = pyshorteners.Shortener(api_key=ACCESS_TOKEN) 
        clean_url = url_shortener.bitly.clean_url(url)
        long_url = url_shortener.bitly.expand(clean_url)
        response = jsonify({'long_url': long_url}), 200
    except (ExpandingErrorException, BadURLException, BadAPIResponseException, Exception ) as e:
        response = {'error': [e.args] }, 500

    return response

@app.route('/')
def index():
    return {"message": "Welcome to URL Shortener service", "supported_urls": ["/shortify?url=xxx", "/logify?url=xxx"]}

if __name__ == '__main__':
    app.run(debug=True)
