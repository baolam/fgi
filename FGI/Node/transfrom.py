from torch import nn

from torch import relu
from torch import rand
from torch import Tensor

from torch import save
from torch import load

from .utils import DT_SAVE
from .utils import DT_FORWARD

class Transfrom(nn.Module):
  SUFFIX = "transfrom"
  
  def __init__(self, da : int, **kwargs):
    super(Transfrom, self).__init__()
    
    self.W = nn.Parameter(rand((1, da)), requires_grad=True)
    self.B = nn.Parameter(rand((1, da)), requires_grad=True)
    
  def forward(self, x : DT_FORWARD) -> DT_FORWARD:
    return relu(
      x * self.W + self.B
    )
  
  def save(self, name : str) -> DT_SAVE:
    file = "{}/{}.pk".format(name, SUFFIX)
    save(self.state_dict, file)
    return file
  
  def load(self, name : str):
    with open(name, "rb", encoding="utf-8") as fin:
      r = load(fin)
    self.load_state_dict(r)