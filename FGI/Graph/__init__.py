from torch import nn
from torch import ones
from torch import zeros

from typing import Dict
from typing import Union

from ..Node import Node
from ..Node import DT_FORWARD
from ..Node import get
from .dfs import DFS

class Graph(nn.Module):
  # Quản lý các đỉnh
  DT_NODE = Dict[int, Node]
  
  # Từ, vị trí trong tập quản ly
  DT_WORD = Dict[str, Union[int, Node]]
  
  def __init__(self, da : int, start_word : str,
    end_word : str):
    super(Graph, self).__init__()
    
    self.da = da  
    self.start_word = start_word
    self.end_word = end_word
    
    self.nodes : DT_NODE = nn.ModuleDict()
    self.words : DT_WORD = dict()
    self.dfs = DFS()
    
    self.words[start_word] = '0'
    self.words[end_word] = '1'
    
    self.nodes['0'] = Node(da = da, f = None, allow_rand = True, word=start_word, id = 0)
    self.nodes['1'] = Node(da = da, f = None, allow_rand = True, word=end_word, id = 1)
    
    self.nodes['0'].add_neigh(f=ones((1, da)), address=id(self.nodes['1']), 
      inp_type = False, weight=None)
    
  def add(self, f : DT_FORWARD, word : str):
    self.dfs.clear()
    
    context = self.__call__(f)
    trace = self.dfs.trace
    
    neighs = self.__maptracetoaddress(trace)
      
    node = Node(f=context, da=self.da, 
      allow_rand=False, id=self.nodes.__len__(), 
      word=word
    )
    
    # Thêm các cạnh tính chất
    for neigh in neighs:
      neigh_node : Node = get(neigh)

      # print("target_word = {}. pred_word = {}".format(node.word, neigh_node.word))
      
      node.add_neigh(neigh_node(context), address=neigh, 
        inp_type=True, weight=None)
      
      # Các đỉnh trong tập neighs sẽ được thêm node đầu vào
      neigh_node.add_neigh(node(context), address=id(node), 
        inp_type=False, weight=None)
    
    # Thêm cạnh kết thúc lan truyền
    node.add_neigh(context, address=id(self.nodes["1"]), 
      inp_type = False, weight = None)
    
    # Thêm đỉnh vào quản lí
    self.nodes[
      str(node.id)
    ] = node
    
    if word != None:
      self.words[word] = str(node.id)
    
  def __maptracetoaddress(self, trace : DFS.DT_TRACE) -> DFS.DT_ADDR:
    r = []
    
    for node in trace:
      r.append(
        id(node)
      )
    
    return r
  
  def forward(self, f : DT_FORWARD):
    self.dfs.clear()
    return self.dfs.forward(f, self.nodes['0'])
    
  def update(self, f : DT_FORWARD):
    for __, node in self.nodes.items():
      node.update(f)
  