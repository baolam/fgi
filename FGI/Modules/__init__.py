from torch import nn
from ..Graph import Graph
from abc import ABC

class Solution(nn.Module):
  def __init__(self, fgi : Graph):
    super(Solution, self).__init__()

    self.fgi = fgi
    
  def get(self, **kwargs):
    # Truy vấn dữ liệu
    pass
  
  def subspect(self, **kwargs):
    # Nghi ngờ
    pass
  
  def saving(self, **kwargs):
    # Lưu trữ
    pass
  
  def passport(self, **kwargs):
    # Chứng thực
    pass
  
  def train(self, **kwargs):
    # Huấn luyện
    pass
  
from .ExistNatureImage import ExistNatureImage
from .Language import Language