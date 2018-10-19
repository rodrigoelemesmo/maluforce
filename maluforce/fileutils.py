import numpy as np
import os
import re

from maluforce.validators import (path_formatter)

SF_BULK_MAX_CHAR = 10000000
SF_BULK_MAX_ITEM = 10000

def num_char(lista):
    """
        Return the number of characters in a list
    """
    all_c = ""
    for i in lista:
        all_c += str(i)
    return len(all_c)


def split_lod_by_char(lod, max_chars=10000000):
    """
        Splits a lod into smaller lods respecting the especified maximum number of characters.
        [input]
        * lod
        * max_chars - maximum number of characters a lod can contain
        [output]
        * list with splited lods
    """
    max_chars = min(max_chars, SF_BULK_MAX_CHAR)
    num_char_item = []
    for item in lod:
        num_char_item.append(num_char([item]))
    num_char_item_cumm = list(np.cumsum(num_char_item))
    x = num_char_item_cumm.copy()
    splited = []
    last = 0
    for i in range(0, len(x) - 1):
        if x[i + 1] > max_chars:
            # print(x[i+1], x[i],i)
            x[i + 1:] = list(np.add(x[i + 1:], [-x[i]] * len(x[i + 1:])))
            x[:i + 1] = [0] * len(x[:i + 1])
            splited.append(lod[last:i + 1])
            last = i + 1
            # print('x depois:',x)
    if last <= len(x):
        splited.append(lod[last:len(x)])
    return splited


def split_lod_by_item(lod, max_items=10000):
    """
        Splits a lod into smaller lods respecting the especified maximum number of items.
        [input]
        * lod
        * max_items
        [output]
        * list with splited lods
    """
    max_items = min(max_items, SF_BULK_MAX_ITEM)
    files = []
    for i in range(0, len(lod), max_items):
        files.append(lod[i:i + max_items])
    return files


def split_lod(lod, max_items=10000, max_chars=10000000):
    """
        Splits a lod into smaller lods respecting the especified maximum number of items anc characters.
        [input]
        * lod 
        * max_items 
        * max_chars
        [output]
        * list with splited lods
    """
    if type(lod) != list:
        raise ValueError("{}: lod must be of type list".format("split_lod"))

    splited_final = []
    for splited_partial in split_lod_by_item(lod, max_items=max_items):
        splited_final.extend(split_lod_by_char(splited_partial, max_chars=max_chars))
    return splited_final


def save_lod_files(files, filename, path=None, start_index=0):
    """
        Saves your lods into .mtxt files
        [input]
        * files - list of lod
        * filename - name template
        * path - path to folder
        * start_index
        [output]
        * files like: filename_[\\d].mtxt
    """
    path = path_formatter(path)
    for i, target in enumerate(files):
        with open("{}{}_{}.mtxt".format(path, filename, i + start_index), "w") as f:
            f.write(str(target))


def read_lod_file(filename):
    with open(filename, "r") as target:
        return eval(target.read())


def read_lod_files(filenames,path=None):
    """
        Carrega os arquivos (.mtxt) da pasta especificada. Os arquivos devem ter indices sequenciais
        [input]
        * path - pasta com os arquivos
        * filenames - list with filenames (.mtxt) to be loaded. (without index, e. g. filename_0.mtxt -> filename)
        [output]
        * dicionario com o {nome dos arquivos (sem indice) : lista dos arquivos}
        Exemplo:
        read_lod_files('Home/','account') carrega account_0.mtxt,account_1.mtxt...
    """
    path = path_formatter(path)
    if type(filenames) != list:
        raise ValueError("{}: filenames invalid parameter!".format("read_lod_files"))
    elif len(filenames) == 0:
        raise ValueError("{}: filenames invalid parameter!".format("read_lod_files"))
    # lists all files in especified path
    dir_files = []
    for __,__,files in os.walk(path):
        for f in files:
            dir_files.append(f)
    # lists .mtxt filenames
    dir_filenames = []
    for f in dir_files:
        dir_filenames.append(re.split("_(\\d)*.mtxt", f)[0])
    # checks validity of input
    if not (set(filenames) < set(dir_filenames)):
        raise ValueError(
            "{}: the files {} were not found on the specified folder!".format(
                "read_lod_files", str(set(filenames) - set(dir_filenames))
            )
        )
    filenames = list(set(filenames))  # remove duplicates
    loaded_files = {}
    for f in filenames:
        loaded_files[f] = []
    for f in dir_files:
        for nome_alvo in filenames:
            if f[:len(nome_alvo)] == nome_alvo:
                load_file = read_lod_file(path + f)
                loaded_files[nome_alvo].append(load_file)
    return loaded_files

