from . import Solution
from ..Graph import Graph
from ..Node import DT_FORWARD
from ..Graph.dfs import DFS

from torch import Tensor
from torch import tensor
from torch import nn
from torch import Tensor
from torch import optim

class Flatten(nn.Module):
  def __init__(self):
    super(Flatten, self).__init__()
    
  def forward(self, x : DT_FORWARD):
    n = x.size()[0]
    return x.reshape((n, -1))

class ExistNatureImage(Solution):
  def __init__(self, fgi : Graph, scale : int):
    super(ExistNature, self).__init__(fgi)
    
    # Tập các tính chất để xác định yếu tố
    # tồn tại
    self.trace = []
    
    flat = 1
    # Trích xuất đặc trưng ảnh
    self.ext_img = nn.Sequential(
      nn.Conv2d(3, 16, 4),
      nn.Conv2d(3, 16, 4),
      nn.ReLU(),
      nn.MaxPool2d((4, 4)),
      nn.Conv2d(16, 16, 4),
      nn.Conv2d(16, 16, 4),
      nn.ReLU(),
      nn.MaxPool2d((4, 4)),
      Flatten(),      
      nn.Linear(flat, flat * scale),
      nn.ReLU(),
      nn.Linear(flat * scale, self.fgi.da),
      nn.ReLU()      
    )
    
    # Mô hình phân loại
    self.using = nn.Sequential(
      nn.Linear(self.fgi.da, 1),
      nn.Sigmoid()
    )
    
  def query(self, img : Tensor) -> DT_FORWARD:
    f = self.ext_img(img)
    return f
  
  def predict(self, img : Tensor) -> DT_FORWARD:
    f = self.query(img)
    f = self.fgi.forward(f)
    f = self.using(f)
    return f
  
  def train(self, x : Tensor, y : Tensor, epochs : int = 20):
    # Trên từng điểm dữ liệu
    e = 1
    loss = nn.BCELoss()
    
    items = []
    while e <= epochs:
      y_pred = self.predict(x)
      optimizer = optim.Adam(self.fgi.parameters())
      l = loss(y_pred, y)
      l.backward()
      optimizer.step()
      items.append(l.item())
      print("e = {}. l = {}".format(e, l.item()))
      e += 1

    self.trace = self.fgi.dfs.trace
    return items
  
  def subspect(self, trace : DFS.DT_TRACE):
    # So sánh dựa vào id 
    na = len(trace)
    nb = len(self.trace)
    
    if na != nb:
      return self.threshold_subspect
    
    return nn.CosineSimilarity()(tensor(trace), tensor(self.trace)).item()   
  
  def run(self, img : Tensor):
    y = self.predict(img)
    phi = self.subspect(
      self.fgi.trace
    )  
    
    return y, phi
  
  def cor_add(self, f : DT_FORWARD):
    self.fgi.add(f, word=None)