from IPython.display import Image
from search_graph import BenimAI
graph = BenimAI().AIBuilder()
with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())