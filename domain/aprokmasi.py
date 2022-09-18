#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from app.libs.utils import safe_float, safe_int
from app.exception.http_error import MultiValidationException

class Aprokmasi(object):
    angka_exp: float
    angka_sign: int
    hasil_angka_exp: float

    def __init__(self, data: dict):
        self.angka_exp = safe_float(data.get("angka_exp", 0))
        self.angka_sign = safe_int(data.get("angka_sign", 0))
        self.hasil_angka_exp = 0

    def prevalidate(self) -> MultiValidationException:
        error = MultiValidationException()

        if self.angka_exp == 0 or self.angka_exp > 50:
            error.push_error("angka_exp", "Invalid input angka exponen. Range input 0.1-50.")
        else:
            self.hasil_angka_exp = safe_float(math.exp(self.angka_exp))

        if self.angka_sign == 0 or self.angka_sign > 50:
            error.push_error("angka_sign", "Invalid input angka signifikan. Range input: 1-50.") 

        return error

    def to_dict(self) -> dict:
        aprokmasi = self.__aprokmasi()
        aprokmasi["e_exp"] = self.hasil_angka_exp
        
        return aprokmasi

    def __aprokmasi(self) -> dict:
        nilai_es = self.angka_exp * math.pow(10, 2-self.angka_sign)
        init_nilai_x = [self.__nilai_x_iterasi1()]
        process = self.__init_process_iterasi(init_nilai_x[0])

        i = 2
        while True:
            x = init_nilai_x.pop()
            nilai_x = safe_float(self.__nilai_x(x, i))
            nilai_et = self.__nilai_et(nilai_x)
            nilai_ea = self.__nilai_ea(nilai_x, x)
            
            process.append({
                "iterasi_ke": i+1,
                "nilai_x": nilai_x,
                "nilai_et": nilai_et,
                "nilai_ea": nilai_ea,
            })
            init_nilai_x.append(nilai_x)
            i += 1

            if nilai_ea < nilai_es:
                break

            if i >= 1000:
                break
        
        result = {
            "process": process,
            "description": f"Jadi, pada iterasi ke-6 diperoleh hasil bahwa e{self.angka_exp} = {nilai_x} dengan error aproksimasi {nilai_ea}% (kurang dari {nilai_es}%)",
            "galat": nilai_es,
        } 

        if i >= 1000:
            result["error"] = True

        return result

    def __nilai_x_iterasi1(self) -> float:
        return 1 + self.angka_exp

    def __init_process_iterasi(self, nilai_x: float = 0) -> list:
        return [
            {
                "iterasi_ke": 1,
                "nilai_x": 1,
            },
            {
                "iterasi_ke": 2,
                "nilai_x": nilai_x,
                "nilai_et": self.__nilai_et(nilai_x),
                "nilai_ea": self.__nilai_ea(nilai_x, 1),
            }
        ]

    def __nilai_x(self, init_nilai_x: float = 0, faktorial: int = 0) -> float:
        angka_exp = math.pow(self.angka_exp, faktorial)
        hasil_faktorial = math.factorial(faktorial)
        result = init_nilai_x + angka_exp / hasil_faktorial

        return result 

    def __nilai_et(self, nilai_x: float = 0) -> float:
        operasi1 = self.hasil_angka_exp - nilai_x
        operasi2 = operasi1 / self.hasil_angka_exp
        
        return self.__to_persen(operasi2)

    def __nilai_ea(self, nilai_x: float = 0, nilai_x_sebelumnya: float = 0) -> float:
        operasi1 = nilai_x - nilai_x_sebelumnya
        operasi2 = operasi1 / nilai_x
        return self.__to_persen(operasi2)

    def __to_persen(self, value: float = 0) -> float:
        data = value*100
        return round(data, 5)
