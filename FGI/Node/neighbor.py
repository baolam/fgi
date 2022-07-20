from torch import nn
from torch import rand
from torch import Tensor
from torch import sigmoid
from torch import softmax
from torch import save
from torch import zeros

from typing import Dict
from typing import Union

from .utils import DT_FORWARD
from .utils import DT_SAVE
from .utils import get

class Edge(nn.Module):
  def __init__(self, da : int, y_hat : DT_FORWARD, **kwargs):
    super(Edge, self).__init__()
    
    w = kwargs.get("weight")
    
    if w == None:    
      self.W = nn.Parameter(rand((1, da)) * y_hat, requires_grad=True)
    else:
      self.W = nn.Parameter(w * rand((1, da)), requires_grad=True)
    
  def forward(self, x : DT_FORWARD, addr : str):
    future = get(
      int(addr)
    )
    
    f = future(x * self.W)
    return (x * f) @ self.W.T
  
class Neighbor(nn.Module):
  DT = Dict[int, Tensor]
  DT_ADDR = Union[int, str]
  SUFFIX = "neighbor"
  
  def __init__(self, da, **kwargs):
    super(Neighbor, self).__init__()

    self.da = da
    self.inps : DT = nn.ModuleDict()
    self.outs : DT = nn.ModuleDict()
  
  def add(self, y_hat : DT_FORWARD, 
    address : DT_ADDR, inp_type : bool, weight : DT_FORWARD):
    """Thêm 1 cạnh

    Args:
      y_hat (DT_FORWARD): Đầu ra lan truyền
      address (DT_ADDR): Địa chỉ ô nhớ của đỉnh muốn thêm
      inp_type (bool): Loại cạnh
    
    More:
      y_hat : Dùng trong việc khởi tạo trọng số của một cạnh
    """
    
    if isinstance(address, int):
      address = str(address)
    
    if inp_type:
      self.inps[address] = Edge(self.da, y_hat, weight=weight)
    else:
      self.outs[address] = Edge(self.da, y_hat, weight=weight)
      
  def rev(self, address : DT_ADDR, inp_type : bool):
    """Xóa một cạnh

    Args:
      address (DT_ADDR): Địa chỉ ô nhớ của đỉnh muốn xóa
      inp_type (bool): Loại cạnh
    """
    if isinstance(address, int):
      address = str(address)
    
    if inp_type:
      self.inps.pop(address)
    else:
      self.outs.pop(address)
      
  def save(self, name : str) -> DT_SAVE:
    file_name = "{}/{}.pk".format(name, SUFFIX)
    save(self.state_dict(destination), file_name)
    return file_name
  
  def forward(self, x : DT_FORWARD, ampli : DT_FORWARD):
    r = zeros((self.outs.__len__()))
    
    i = 0
    for addr, edge in self.outs.items():
      r[i] = edge(x, addr) * ampli
      i += 1
    
    r = softmax(r, dim=0)
    return r
  
  def sfm(self, idx : int) -> DT_FORWARD:
    addr, edge = list(self.outs.items())[idx]
    return addr, edge.W