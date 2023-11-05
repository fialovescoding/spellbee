from random import randint
import time
import hashlib
import pickle
import os
import numpy as np
import pandas as pd
import sys
from datetime import datetime, timedelta
import yaml

def time_uid() -> int:
    """Generates a time dependent unique-id"""
    ts = int(time.time()) # limit to recent
    randid = randint(0, 511)
    ts = (ts * 64)   # bit-shift << 6
    return (ts * 512) + randid

# REF: https://stackoverflow.com/questions/14023350/cheap-mapping-of-string-to-small-fixed-length-string
def cheaphash(string,length=6):
    if len(string) < length:
        return string
    
    _hash = hashlib.sha256(string.encode('utf-8')).hexdigest()
    if length<len(_hash):
        return _hash[:length]
    else:
        raise Exception("Length too long. Length of {y} when hash length is {x}.".format(x=str(len(hashlib.sha256(string).hexdigest())),y=length))
    
def PickleObject(fpath: str, obj):
    fh = open(fpath, 'ab')  # Open in append/binary mode
    pickle.dump(obj, fh)
    fh.close()

def GetPickledObj(fpath: str):
    fh = open(fpath, 'rb')  # Open in read/binary mode
    obj = pickle.load(fh)
    fh.close()
    return obj

def FindFirstIdxDs(ds: pd.Series, val):
    search = np.where(ds == val)
    idx = search[0][0] if(len(search[0]) >= 1) else None
    return idx

def GetFullPath(rel_path):
    # Expand rel_path in case a list of relative path elements and then join
    # REF: https://stackoverflow.com/questions/4934806/how-can-i-find-scripts-directory
    base = os.path.abspath(os.path.dirname(sys.path[0]))
    # print('Base directory: ', base, os.getcwd())
    # print('rel_path: ', rel_path)
    # file_dir = os.path.dirname(__file__)
    if(type(rel_path) is list):
        return os.path.join(base, *rel_path)
    else:
        return os.path.join(base, rel_path)
    
def ReadConfig(secrets: bool = False) -> dict:
    # Import Config
    if secrets:
        fpath = 'config/secrets.yaml'
    else:
        fpath = 'config/app.yaml'

    config = yaml.safe_load(open(GetFullPath(fpath)))

    if type is not None:
        return config

    return config

def clamp(n, nmin, nmax):
    """Returns the number n after clamping between nmin and nmax"""
    return (max(nmin, min(n, nmax)))

def ReadTextFromFile(fpath, relpath=True):
    if relpath:
        fpath = GetFullPath(fpath)
    return open(fpath, 'r').read()

def enum_as_dict(enum_cls):
    """Returns all items in enum_cls class as enum.value: enum.name pairs. This can be used in nicegui drop-down selection to show names of Enum"""
    return {i.value: i.name for i in enum_cls}

def get_date_as_str(days_from_today: int = 0, fmt: str = 'YYYY-mm-dd'):
    return (datetime.today() + timedelta(days=days_from_today)).strftime(fmt)

def get_midnight_timestamp(dt: datetime) -> float:
    """Returns the timestamp at midnight, ignoring time component of df"""
    return datetime(dt.year, dt.month, dt.day).timestamp()

def formatFloat(val, as_pct=False):
    if(type(val) is float):
        if as_pct == False:
            return "{:.1f}".format(val)
        else:
            # % format multiplies by 100, so need to divide
            return "{:.1%}".format(val / 100)
    else:
        return val