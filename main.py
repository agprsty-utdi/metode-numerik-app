#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, jsonify, render_template, request
from app.error import register_error_handler
from app.exception.http_error import BadRequestException
from app.libs.utils import safe_int
from domain.aprokmasi import Aprokmasi

os.environ.get("FLASK_ENV", default="production")
app = Flask(__name__)
app = register_error_handler(app)
app.config.from_pyfile(f'{os.getcwd()}/config/config.py')

base_url = app.config.get("GENERAL").get("base_url")

@app.route('/', methods=["GET"])
def welcome_view():
    return render_template(
        "welcome.html",
        title="Welcome",
        base_url=base_url
    )

@app.route('/aproksimasi', methods=["GET"])
def aprokmasi_view():
    return render_template(
        "aprokmasi.html", 
        title="Aproksimasi",
        base_url=base_url
    )

@app.route('/aproksimasi', methods=["POST"])
def aprokmasi():
    data = __get_form_json_input(request.json)
    
    aprokmasi = Aprokmasi(data)
    error = aprokmasi.prevalidate()
    if not error.is_empty():
        raise error

    result = aprokmasi.to_dict()
    if __check_operation_error(result):
        raise BadRequestException("Because too many process, force break in index 1000")

    return jsonify({
        "meta": {
            "status": 200,
            "code": "success",
            "message": "ok"
        },
        "data": result,
    })

def __get_form_json_input(args: dict)->dict:
    """Form json input"""
    return {
        "angka_exp": args.get("exponen", 0),
        "angka_sign": args.get("signifikan", 0)
    }

def __check_operation_error(data: dict) -> bool:
    """Check if "error_operation" is none or not"""
    result = False
    if "error" in data:
        result = True

    return result

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0', 
        port=safe_int(
            app.config\
                .get("GENERAL", {})\
                .get("app_port", 8000)
        )
    )