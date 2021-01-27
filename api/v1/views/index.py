#!/usr/bin/python
"""
Display status code.
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def display_status():
    """
    Return status code OK
    """
    return jsonify({"status": "OK"})
