from torch import Tensor

import ctypes

def get(address : int):
  return ctypes.cast(address, ctypes.py_object) \
    .value

def strtoint(address : str):
  return int(address)

DT_SAVE = str
DT_FORWARD = Tensor
