from torch import nn

from torch import sigmoid
from torch import rand
from torch import Tensor

from torch import save
from torch import load

from .utils import DT_SAVE
from .utils import DT_FORWARD

class Attention(nn.Module):
  SUFFIX = "attention"
  
  def __init__(self, da : int, **kwargs):
    super(Attention, self).__init__()
    
    self.W = nn.Parameter(rand((1, da)), requires_grad=True)
    self.b = nn.Parameter(rand(1), requires_grad=True)
    
  def forward(self, x : DT_FORWARD) -> DT_FORWARD:
    return sigmoid(
      x @ self.W.T + self.b
    )
  
  def save(self, name : str) -> DT_SAVE:
    file = "{}/{}.pk".format(name, SUFFIX)
    save(self.state_dict, file)
    return file
  
  def load(self, name : str):
    with open(name, "rb", encoding="utf-8") as fin:
      r = load(fin)
    self.load_state_dict(r)