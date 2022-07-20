import os
from torch import nn
from torch import zeros
from torch import rand

from .nature import Nature
from .attention import Attention
from .transfrom import Transfrom
from .neighbor import Neighbor

from .utils import DT_FORWARD
from .utils import DT_SAVE

class Node(nn.Module):
  SUFFIX = "node"
  
  def __init__(self, **kwargs):
    super(Node, self).__init__()
    
    self.id = kwargs.get("id")
    self.word = kwargs.get("word")
    self.da = kwargs.get("da")
    
    self.ampli = nn.Parameter(rand((1)), requires_grad=True)
    self.__nature = Nature(**kwargs)
    self.__attention = Attention(**kwargs)
    self.__transfrom = Transfrom(**kwargs)
    self.__neighbor = Neighbor(**kwargs)
    
  def nature(self) -> DT_FORWARD:
    return self.__nature.n
  
  def neighbor(self):
    return self.__neighbor.inps, self.__neighbor.outs
  
  def forward(self, x : DT_FORWARD) -> DT_FORWARD:
    n = self.__nature(x)
    n = self.__transfrom(n)
    a = self.__attention(n)
    return n * a
  
  def move_probability(self, f : DT_FORWARD, ampli : DT_FORWARD):
    y = self.__call__(f)
    return self.__neighbor(y, ampli)
  
  def edge(self, idx : int) -> DT_FORWARD:
    return self.__neighbor.sfm(idx)
  
  def add_neigh(self, f : DT_FORWARD, weight : DT_FORWARD, **kwargs):
    # f là đặc trưng đầu vào
    # sinh trọng số dựa vào đây
    if weight == None:
      y = self.__call__(f)
    else:
      y = weight
      
    self.__neighbor.add(y, weight=weight, **kwargs)
    
    if kwargs.get("inp_type"):
      if f == None:
        f = zeros((1, self.da))
      self.update(f)
      
  def update(self, f : DT_FORWARD):
    # Cập nhật tính chất dựa vào đặc trưng đầu vào
    # và tập các đỉnh tạo nên tính chất đó
    self.__nature.update(f=f, neighs=self.__neighbor.inps)
    
  def save(self, name : str) -> DT_SAVE:
    folder_name = "{}/{}_{}".format(name, SUFFIX, self.id)
    
    if os.path.exists(folder_name) == False:
      os.makedirs(folder_name)
    
    self.__nature.save(folder_name)
    self.__transfrom.save(folder_name)
    self.__attention.save(folder_name)
    self.__neighbor.save(folder_name)
  
from .utils import *