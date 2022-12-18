#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from app.libs.utils import safe_int
from app.exception.http_error import MultiValidationException

INPUT = {
    "X": [10, 20, 30, 40, 50, 60, 70],
    "Y": [12, 21, 46, 65, 90, 111, 148]
}

class PolinomialNewton(object):
    xinput: int

    def __init__(self, data: dict) -> object:
        self.xinput = safe_int(data.get("xinput", 0))
    
    def prevalidate(self) -> MultiValidationException:
        error = MultiValidationException()

        if self.xinput == 0 or \
            (self.xinput < 10 or self.xinput > 70):
            error.push_error("input", "Invalid input. Range input: 10-70")

        return error

    def to_dict(self) -> dict:
        return self.__polinom_newton()

    def __polinom_newton(self) -> dict:
        x = INPUT["X"]
        y = INPUT["Y"]
        n = len(x)-1
        ST = np.zeros((n+1, n+1))
        ST[:, 0] = y

        for k in range(1, n+1):
            for i in range(0, n-k+1):
                ST[i, k] = round((ST[i+1, k-1] - ST[i, k-1])/(x[i+k]-x[i]), 5)

        p = ST[0,0]
        for i in range(1, n+1):
            a = ST[0, i]

            for k in range(0, i):
                a = a * (self.xinput-x[k])

            p = p + a
        
        return {
            "calculate": ST.tolist(),
            "result": p,
        }
