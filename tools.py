from duckduckgo_search import DDGS
from phi.tools import Toolkit

class SupplyChainTools(Toolkit):
    def __init__(self):
        super().__init__(name="supply_chain_tools")
        self.register(self.search_news)

    def search_news(self, query: str, max_results: int = 5):
        """
        Searches for news articles related to the query using DuckDuckGo.
        
        Args:
            query (str): The search query (e.g., "Lithium supply chain shortage").
            max_results (int): Maximum number of results to return.
            
        Returns:
            list: A list of dictionaries containing title, body, and url.
        """
        results = []
        try:
            with DDGS() as ddgs:
                ddgs_gen = ddgs.news(query, max_results=max_results)
                for r in ddgs_gen:
                    results.append(r)
        except Exception as e:
            return f"Error searching news: {e}"
        return results
