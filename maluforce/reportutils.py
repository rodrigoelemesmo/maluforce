import copy
import pandas as pd
from collections import OrderedDict

def adjust_report(report,utf_encoded=False):
    """ 
        Adjusts a Salesforce dml operation response into a pandas.DataFrame utf-8 encoded for .xlsx compatibility
    """
    s = []
    a = copy.deepcopy(report)
    for i in a:
        if "errors" in i.keys():
            if not i["errors"]:
                del i["errors"]
                s.append(i)
            else:
                i["message"] = i["errors"][0]["message"]
                del i["errors"]
                s.append(i)
        else:
            s.append(i)
    dataframe = pd.DataFrame(s)
    if utf_encoded:
        dataframe = dataframe.applymap(
            lambda x: x.encode("unicode_escape").decode("utf-8")
            if isinstance(x, str)
            else x
        )
    return dataframe


def lod_rename(lod, key_map, drop=False):
    """
        [input]
        * lod - lod with keys to be renamed
        * key_map - dict, {"old_key": "new_key"}
        * drop - True to drop keys that are not in key_map
        [output]
        * lod - with renamed keys
    """
    return to_lod(pd.DataFrame(lod),key_map=key_map, drop=drop)


def to_lod(df, key_map=None, drop=False):
    """
        [input]
        * key_map - dict, {"old_key": "new_key"}
        * drop - True to drop columns that are not in key_map
        [output]
        * lod - with renamed keys
    """
    df_copy = copy.deepcopy(df)
    if key_map == None:
        out = df_copy.to_dict(orient="records")
    else:
        keys_not_found = set(key_map.keys()) - set(df_copy.columns)
        colm_not_in_map = set(df_copy.columns) - set(key_map.keys())
        if len(keys_not_found) != 0:
            raise ValueError(
                "The following keys were not found in the data: {}".format(
                    keys_not_found
                )
            )
        if len(colm_not_in_map) > 0 and (not drop):
            raise ValueError(
                "The following were not found on the key_map.keys(). Set drop to True to drop them: {}".format(
                    colm_not_in_map
                )
            )
        df_new_columns = df_copy.rename(index=str, columns=key_map, copy=True)
        if drop:
            df_new_columns.drop(
                columns=list(set(df_new_columns.columns) - set(key_map.values())),
                inplace=True,
            )
        out = df_new_columns.to_dict(orient="records")
    return out


def decodeSFresponse(resp):
    out = []
    for root in resp:
        out.extend([decodeSFObject(root)])
    return out


def decodeSFObject(root):
    dict_node = {}
    for node in list(set(root.keys()) - {"attributes"}):
        if type(root[node]) in [OrderedDict,dict]:
            tmp = {}
            tmp = decodeSFObject(root[node])
            for sub in tmp:
                dict_node[node + sub] = tmp[sub]
        else:
            dict_node[node] = root[node]
    return dict_node

def to_unicode(df):
    out = df.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
    return out
