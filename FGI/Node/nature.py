from torch import nn
from torch import Tensor
from torch import rand
from torch import tanh
from torch import save
from torch import load

from typing import Dict

from .utils import get
from .utils import DT_SAVE
from .utils import DT_FORWARD

class Nature(nn.Module):
  SUFFIX = "nature"
  
  # địa chỉ ô nhớ, trọng số
  DT_NEIGHBS = Dict[int, Tensor]
  
  def __init__(self, da : int, f : DT_FORWARD, 
    allow_rand : bool, **kwargs):
    super(Nature, self).__init__()
    
    if allow_rand:
      self.n = nn.Parameter(rand((1, da)), requires_grad=True)
    else:
      self.n = nn.Parameter(f, requires_grad=True)
      
  def initalize(self, f : DT_FORWARD, neighs : DT_NEIGHBS) -> DT_FORWARD:
    for address, edge in neighs.items():
      my_neighbor = get(int(address))
      f = f + my_neighbor.nature() * edge.W
    f = tanh(f)
    return f
  
  def update(self, **kwargs):
    self.n = nn.Parameter(self.initalize(**kwargs), requires_grad=True)
  
  def forward(self, x : DT_FORWARD) -> DT_FORWARD:
    return x * self.n
    
  def save(self, name : str) -> DT_SAVE:
    file_name = "{}/{}.pk".format(name, SUFFIX)
    save(self.state_dict(), file_name)
    return file_name
  
  def load(self, name : DT_SAVE):
    with open(name, "rb", encoding="utf-8") as fin:
      r = load(fin)
    self.load_state_dict(r)