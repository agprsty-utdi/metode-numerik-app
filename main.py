#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from app.error import register_error_handler
from app.exception.http_error import BadRequestException
from logic.aprokmasi import Aprokmasi

app = Flask(__name__)
app = register_error_handler(app)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/aprokmasi', methods=["POST"])
def aprokmasi():
    data = __get_form_json_input(request.json)
    
    aprokmasi = Aprokmasi(data)
    error = aprokmasi.prevalidate()
    if not error.is_empty():
        raise error

    result = aprokmasi.to_dict()
    if __check_operation_error(result.get("hasil")):
        raise BadRequestException("Because too many request, force break in index 100")

    return jsonify({
        "meta": {
            "status": 200,
            "code": "success",
            "message": "ok"
        },
        "data": result,
    })

def __get_form_json_input(args: dict)->dict:
    return {
        "angka_exp": args.get("exponen", 0),
        "angka_sign": args.get("signifikan", 0)
    }

def __check_operation_error(data: dict) -> bool:
    result = False

    # check if "error_operation" is none or not.
    if "error" in data:
        result = True

    return result