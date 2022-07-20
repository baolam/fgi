from torch import save
from FGI import Graph
from FGI import Language

fgi = Graph(128, "statsta", "endend")
lang = Language(fgi)

lang.run("lâm dễ thương lắm nhe")

save(lang.state_dict(), "l.pk")