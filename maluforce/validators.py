import re
import os

def validId(id):
    """
        [input]
        * id - str, list with the affiliation_id to be evaluated
        [output]
        * list - ['Pagar.me','Mundi','Stone',None]
    """
    strFlag = False
    if type(id) is str:
        id = [id]
        strFlag = True
    out = [None] * len(id)
    re_map = {"Pagar.me":"[a-f\\d]{24}", "Mundi":"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}","Stone":"[\\d]+"}
    for index, value in enumerate(id):
        for re_test in re_map:
            if bool(re.fullmatch(re_map[re_test],value)):
                out[index] = re_test
    return out[0] if strFlag else out 

def fixCNPJ(cnpj, n):
    b = str(cnpj)
    while len(b) < n:
        b = "0" + b
    return b


def path_formatter(path):
    if path is not None:
        if path[-1] != "/":
            raise ValueError("The given path does not point to a folder. Be sure to append '/' at its end.")
    else:
        path = os.getcwd() + "/"
    return path