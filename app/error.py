#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .exception.http_error import HttpException
from flask import Flask, jsonify
import logging

log = logging.getLogger(__name__)

def register_error_handler(app: Flask):
    @app.errorhandler(HttpException)
    def handle_http_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        log.exception(error.message)
        return response 
    
    @app.errorhandler(Exception)
    def handle_default_error(error):
        code = getattr(error, "code", 500)
        message = getattr(error, "description", "Internal Server Error")
        response = jsonify({
            "meta": {
                "code": code,
                "message": message
            }        
        })
        response.status_code = code
        log.exception(message)
        return response 
    
    return app
    