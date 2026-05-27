from typing import Optional, Literal
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv(override = True)

client = TavilyClient()

def tavily_search_tool(query: str, 
    topic: Literal["general", "news", "finance"] = "general",
    max_results: int = 2,
    search_depth: Literal["fast", "ultra-fast", "advenced", "basic"] = "fast", 
    include_raw_content: bool = False
    ) -> dict:
    """ 
        Makes a websearch. 
    
        Args:
            query: Aranacak veriyi temsil eder.
            topic: Yapılacak aramanın topic i. Sadece "general", "news", "finance" değerlerini Literal olarak alır. 
                Girilmezse general olarak çalışır. User isteğine göre güncellenebilir.
            max_results: Kaç arama sonucu döneceğini belirler. Eğer çıktıyı beğenmezsen toolu daha 
                büyük bir max_result değeriyle tekrardan çalıştır.
            search_depth: Arama derinliğini temsil eder. default olarak basic değerini alır. Alabileceği değerler:
                "fast", "ultra-fast", "advenced", "basic"
            include_raw_content: Raw contentin döndürülüp döndürülmeyeceğini belirler. Default olarak False tur. 
    """

    return client.search(
        query = query,
        topic = topic,
        max_results = max_results,
        search_depth = search_depth,
        include_raw_content = include_raw_content
    )

