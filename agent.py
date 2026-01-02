from phi.agent import Agent
from phi.model.openai import OpenAIChat
from supply_chain_watchdog.tools import SupplyChainTools
import os
from dotenv import load_dotenv

load_dotenv()

def get_supply_chain_agent(model_id="gpt-4o"):
    """
    Returns a configured Phidata Agent for supply chain risk analysis.
    """
    return Agent(
        name="Supply Chain Watchdog",
        model=OpenAIChat(id=model_id),
        tools=[SupplyChainTools()],
        instructions=[
            "You are an autonomous supply chain risk analyst.",
            "Your goal is to monitor news and assess risks for specific commodities or companies.",
            "When received a query, use the `search_news` tool to find the latest relevant information (limit to 5-10 results).",
            "Synthesize the gathered information into a comprehensive report.",
            "Your report MUST include:",
            "1. **Risk Level**: Clearly state (Low, Medium, High).",
            "2. **Key Drivers**: What factors are influencing this risk (e.g., strikes, shortages, policy).",
            "3. **Summary**: A detailed summary of the news findings with citations if possible.",
            "4. **Actionable Advice**: What should supply chain managers do?",
            "Be professional, concise, and data-driven in your analysis."
        ],
        show_tool_calls=True,
        markdown=True,
    )
