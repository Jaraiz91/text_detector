
import psycopg2
from psycopg2.extensions import  AsIs
import numpy as np

def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

def adapt_array(a):
    return psycopg2.Binary(a)


def typecast_array(data, cur):
    if data is None: return None
    buf = psycopg2.BINARY(data, cur)
    return np.frombuffer(buf)
