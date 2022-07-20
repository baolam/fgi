from . import Solution
from torch import rand
from torch import ones
from torch import nn
from torch import zeros
from torch import optim

from ..Graph import Graph
from ..Node import Node
from .. Node import DT_FORWARD
from ..Graph import DFS

from typing import List
from typing import Tuple
from typing import Dict

class Language(Solution):
  FILTER = "1234567890-=!@#$%^&*()_+[]\;',./{|}:<>?"
  DT_INP = List[int]
  DT_FAKE_ADDR = Dict[int, str]
  DT_OUT = List[str]
  
  def __init__(self, fgi : Graph):
    super(Language, self).__init__(fgi)
  
    # Mô hình huấn luyện ngôn ngữ
    self.ok = nn.Sequential(
      nn.Linear(self.fgi.da, 1),
      nn.Sigmoid()
    )
    
    self.params = []
        
  def preprocessing(self, x : str) -> DT_INP:
    for char in Language.FILTER:
      x = x.replace(char, '')
    x = x.lower()
    y = x.split()
    
    # Thêm 2 từ mặc định
    y.insert(0, self.fgi.start_word)
    y.append(self.fgi.end_word)
    
    return self.__empty(y)
  
  def word_inp(self, x : str, f : DT_FORWARD) -> Tuple[DT_FORWARD, DT_OUT]:
    # Đầu vào là từ ngữ
    y = self.preprocessing(x)

    # ------------------------
    # Xây dựng bộ từ ngữ chưa biết
    self.ureal_build(y)
    
    if f == None:
      f = ones((1, self.fgi.da))

    # f là đặc trưng bổ sung
    context = self.wdfs(y, f)

    # y đây là kết quả của quá trình xác định
    # tồn tại tính chất
    y = self.fgi.forward(context)
    tracing = self.fgi.dfs.trace
    
    return y, self.decode(tracing)
  
  def subspect(self, y : DT_FORWARD):
    # Xác định nghi ngờ bằng 1 mạng lan truyền
    # đơn giản
    # Việc xây dựng hàm lỗi tối ưu cũng sẽ dựa 
    # vào đây
    return self.ok(y)
  
  def decode(self, trace : DFS.DT_TRACE) -> DT_OUT:
    r = []
    
    for node in trace:
      r.append(
        node.word
      )

    return r
  
  def ureal_build(self, y : DT_OUT):
    context = ones((1, self.fgi.da))
        
    for i in range(len(y) - 1):
      word = y[i]
      future_word = y[i + 1]
            
      context, node = self.transformctx(word, context)
      weight = rand((1, self.fgi.da)) * context
      
      context, future_node = self.transformctx(future_word, context * weight)
            
      node.add_neigh(f=None, address=id(future_node), inp_type=False, weight=weight)
      future_node.add_neigh(f=None, address=id(node), weight=rand((1, self.fgi.da)) * context, inp_type=True)

      context = context * weight
      
  def wdfs(self, y : DT_INP, f : DT_FORWARD, step : int = 0):  
    # Duyệt để tạo ngữ cảnh
    if step == len(y) - 2:
      return f

    node : Node = self.fgi.nodes[
      self.fgi.words[
        y[step]
      ]
    ]
    
    # -----------------------------------
    # Lấy trọng số cạnh :>s
    future_node : Node = self.fgi.nodes[
      self.fgi.words[
        y[step + 1]
      ]
    ]
    
    __, outs = node.neighbor()
    edge = outs[
      str(id(future_node))
    ]
    
    params = node.parameters()
    for param in list(params):
      self.params.append(param)
    self.params.append(edge.W)
    # ------------------------------------
    
    f = node(f) * edge.W
    return self.wdfs(y, f, step + 1)
    
  def transformctx(self, word : str, ctx : DT_FORWARD) -> Tuple[DT_FORWARD, Node]:
    # Vị trí trong mảng quản lí
    position = self.fgi.words.get(word)
    
    if position == None:  
      self.fgi.add(ctx, word)
      position = self.fgi.words.get(word)
    
    node = self.fgi.nodes[position] 
    
    return node(ctx), node
  
  def __empty(self, y : DT_INP) -> DT_INP:
    r = []
    for word in y:
      if word != '':
        r.append(word)
    return r
  
  def run(self, x : str, f : DT_FORWARD = None):
    # Hàm chạy kết quả
    # phi cho biết về độ tự tin của dự đoán
    y, sens = self.word_inp(x, f)
    phi = self.subspect(y)
    return phi, sens
  
  def train(self, x : str, y : str, f : DT_FORWARD = None ,epochs : int = 10):
    y_train = self.preprocessing(y)
    y_train = y_train[0:len(y_train) - 1]
    
    losses = []
    e = 1
    
    while e <= epochs:
      s, sen = self.run(x, f)
      s_hat = s.reshape(-1)
      
      subspect_train, ps_train = self.buildtraing(y=y_train, sen=sen)
      mps_hat = self.fgi.dfs.mps
      
      adam = optim.Adam(self.parameters())
      l = self.combine_loss(subspect_train=subspect_train, 
        ps_train=ps_train, mps_hat=mps_hat, s_hat=s_hat)
      l.backward()
      adam.step()
      self.fgi.update(zeros((1, self.fgi.da)))
      
      print("e = {}. l = {}. threshold = {}. sen = {}" \
        .format(e, l.item(), s_hat.item(), sen))
      
      losses.append(
        l.item()
      )
      
      e += 1

    return losses
  
  def __subspect(self, sen : DT_OUT, y : DT_OUT) -> DT_FORWARD:
    z = zeros((1))

    is_ok = 1.
    
    if len(sen) != len(y):
      is_ok = 0.
    else:
      for i in range(len(sen)):
        if sen[i] != y[i]:
          is_ok = 0.
          break
    
    z[0] = is_ok
    return z
  
  def buildtraing(self, **kwargs) \
    -> Tuple[DT_FORWARD, List[DT_FORWARD]]:
    s = self.__subspect(**kwargs)
    
    y = kwargs.get("y")
    sen = kwargs.get("sen")
    
    score = min(len(y), len(sen))
    if score == len(y):
      score -= 1
    
    ps = []
    for i in range(score):
      if y[i] != sen[i]:
        break
      current_word, future_word = y[i], y[i + 1]
      ps.append(
        self.build_one_hot(current_word, future_word)
      )
    
    return s, ps
  
  def build_one_hot(self, current : str, future : str):
    node : Node = self.fgi.nodes[
      self.fgi.words[current]
    ]

    # Lấy địa chỉ ô nhớ của đỉnh tương lai
    future_id = id(
      self.fgi.nodes[
        self.fgi.words[future]
      ]
    )
    
    # Tập đỉnh ra của đỉnh hiện tại (current)
    __, outs = node.neighbor()
    
    # Vector one hot
    n = outs.__len__()
    z = zeros((n))
    i = 0
    
    for addr, __ in outs.items():
      if future_id == int(addr):
        break
      i += 1
    
    z[i] = 1.
    return z
  
  def combine_loss(self, **kwargs) -> DT_FORWARD:
    subspect_train = kwargs.get("subspect_train")
    s_hat = kwargs.get("s_hat")
    
    loss = nn.BCELoss()
    l_subspect = loss(s_hat, subspect_train)
    
    ps_train = kwargs.get("ps_train")
    mps_hat = kwargs.get("mps_hat")
    
    l_mp = 0.
    for i in range(len(ps_train)):
      y_train = ps_train[i]
      y_hat = mps_hat[i]
      
      l_mp += loss(y_hat, y_train)
    
    return l_subspect * (l_mp / len(ps_train))  