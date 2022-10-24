# A very simple Flask Hello World app for you to get started with...
import json

import flask
from flask import Flask, jsonify, request
import cluster

app = Flask(__name__)


@app.route('/mid-clusters', methods=['GET'])
def get_mid_clusters():
    try:
        # We require three arguments to the endpoint:
        #   - start_year (int)
        #   - end_year (int)
        #   - country (string)
        #   - size (float from 0 to 1)
        start_year = int(request.args.get('start_year'))
        end_year = int(request.args.get('end_year'))
        country = request.args.get('country')
        size = float(request.args.get('size'))
        assert 0 <= size <= 1
    except Exception:
        # We could not find the required arguments
        response = flask.make_response("Invalid request", 400)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        this_cluster, that_cluster = cluster.find_mid_clusters(start_year, end_year, country, size)
    except Exception:
        # We could not find the clusters
        response = flask.make_response("Internal error", 500)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # Everything looks good - return the answer
    response = jsonify({'this_cluster': this_cluster,
                        'that_cluster': that_cluster})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
