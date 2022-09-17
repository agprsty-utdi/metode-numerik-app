#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import BaseException

class HttpException(BaseException):
    payload = {}
    def __init__(self, message = None)->None:
        if message :
            self.message = message
        super().__init__(self.message)

    def to_dict(self)->dict:
        response = {
            'code': self.status_code,
            'message': self.message
        }
        
        if self.payload.get("error", None):
            response.update(self.payload)
        return {
            "meta": response
        }

class InternalServerErrorException(HttpException):
    message = 'Internal Server Error'
    status_code = 500
    def __init__(self, message = None)->None:
        if message :
            self.message = message
        super().__init__(self.message)

class NotFoundException(HttpException):
    message = 'Not found'
    status_code = 404
    def __init__(self, message = None)->None:
        if message :
            self.message = message
        super().__init__(self.message)

class UnauthorizedException(HttpException):
    message = 'Unauthorized'
    status_code = 401
    def __init__(self, message = None)->None:
        if message :
            self.message = message
        super().__init__(self.message)

class ForbiddenException(HttpException):
    message = 'Forbidden'
    status_code = 403
    def __init__(self, message = None)->None:
        if message :
            self.message = message
        super().__init__(self.message)

class BadRequestException(HttpException):
    message = 'Forbidden'
    status_code = 400
    def __init__(self, message = None)->None:
        if message :
            self.message = message
        super().__init__(self.message)

class MultiValidationException(HttpException):
    message = 'Bad Request'
    status_code = 400
    payload = {}

    def __init__(self, message = None)->None:
        if message :
            self.message = message
        self.payload['error'] = {}
        super().__init__(self.message)

    def set(self, errors):
        for key in errors:
            self.push_error(key, errors[key])

    def push_error(
        self,
        field: str,
        error: str or list
    )->None:
        if field not in self.payload['error']:
            self.payload['error'][field] = []
        if isinstance(error, list):
            self.payload['error'][field].extend(error)
        else:    
            self.payload['error'][field].append(error)
        
    def is_empty(self)->bool:
        if self.payload['error']:
            return False

        return True
