from .graph_scraper import build_graph_for_scrape
from .graph_scraper import chat_with_ai
from schemas_scraper import InstagramState

if __name__ == "__main__":
    try:
        graph = build_graph_for_scrape(InstagramState)
        user_prompt = input("LLM e instagram hesabını ve isteğinizi yazınız: ")
        print(chat_with_ai(graph, user_prompt))

    except Exception as e:
        print(f"Hata: {e}")