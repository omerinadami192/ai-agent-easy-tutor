from IPython.display import Image
from graph_scraper import build_graph_for_scrape
from schemas_scraper import InstagramState

graph = build_graph_for_scrape()
with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())
