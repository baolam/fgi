STEPS = 250

from torch import argmax
from torch import sigmoid
from torch import nn
from torch import mean
from torch import Tensor

from ..Node import Node
from ..Node import DT_FORWARD
from ..Node import get

from typing import List

class DFS():
  DT_TRACE = List[Node]
  DT_ADDR = List[int]
  DT_MP = List[Tensor]
  
  def __init__(self):
    self.trace : DT_TRACE = []
    self.mps : DT_MP = []
    self.met = []
    self.steps = 0
       
  def forward(self, f : DT_FORWARD, node : Node) -> DT_FORWARD:
    mp = node.move_probability(f, node.ampli)
    
    # Xác suất chuyển đỉnh
    self.mps.append(mp)
    
    if node.id == 1:
      return f
        
    idx = argmax(mp).item()
    addr, __ =  node.edge(idx)
    
    self.steps += 1
    self._sort(id(node))
    self.trace.append(node)

    f = f * mp[idx]
    if self.steps == STEPS or self._search(int(addr)):
      return f

    return self.forward(f, get(int(addr)))

  def clear(self):  
    self.trace.clear()
    self.met.clear()
    self.mps.clear()
    self.steps = 0
    
  def _sort(self, new_address : int):
    """Thuật toán sắp xếp dựa vào con trỏ

    Args:
      new_address (int): Địa chỉ ô nhớ
    """
    l = 0

    # Kiếm vị trí đầu tiên lớn hơn giá trị new_address
    while l <= len(self.met) - 1 and self.met[l] < new_address:
      l += 1
    
    # Cho phần tử vào vị trí
    self.met.insert(l, new_address)
    
  def _search(self, addr : int) -> bool:
    """Thuật toán tìm kiếm nhị phân, tìm địa chỉ ô nhớ

    Args:
      addr (int): Địa chỉ ô nhớ

    Returns:
      bool: Có tồn tại hay không
    """
    l = 0
    r = len(self.met) - 1
    
    while l <= r:
      m = int((l + r) / 2)
      if self.met[m] == addr:
        return True
      if self.met[m] < addr: 
        l = m + 1
      else:
        r = m - 1
    
    return False
