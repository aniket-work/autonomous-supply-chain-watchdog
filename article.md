---
title: "Building an Autonomous Supply Chain Watchdog: My Experiment with AI Reasoning Agents"
subtitle: "How I built a real-world vigilant AI agent to solve complex supply chain business problems using Phidata and GPT-4o"
published: true
tags: ai, python, machinelearning, agents
cover_image: https://raw.githubusercontent.com/aniket-work/autonomous-supply-chain-watchdog/main/images/title_diagram.png?v=1
---

![Title Diagram](https://raw.githubusercontent.com/aniket-work/autonomous-supply-chain-watchdog/main/images/title_diagram.png?v=1)

## TL;DR

In this experimental post, I didn't just want to build another chatbot; I wanted to solve a genuine business headache: **Supply Chain Visibility**. I built an "Autonomous Supply Chain Watchdog" using **Phidata** and **GPT-4o** that proactively scans the web for news, reasons about its impact on specific commodities (like Lithium or Cobalt), and generates risk assessments. It's not just a search wrapper; it's a reasoning engine. I’ve open-sourced the entire project, and in this article, I’ll walk you through exactly how I built it, step-by-step.

**The Code**: [https://github.com/aniket-work/autonomous-supply-chain-watchdog](https://github.com/aniket-work/autonomous-supply-chain-watchdog)

---

## Introduction

I have been observing the AI agent space for a while now, and in my opinion, we are stuck in a "toy phase." We see endless demos of agents planning vacations or writing poems, but as per my experience working with enterprise systems, businesses don't need poems. They need **reliability** and **actionable intelligence**.

One area I have always found fascinating is the global supply chain. It's fragile. A single strike in a port in Australia or a policy change in Chile can send shockwaves through the electric vehicle market. I thought to myself: *Why does a human analyst have to manually Google this every morning?*

I decided to run an experiment. Could I build an AI agent that doesn't just "chat" but actually *acts* as a watchdog? An agent that wakes up, looks for trouble, analyzes it with the skepticism of a risk manager, and reports back?

I wrote this article to document my journey building this **Autonomous Supply Chain Watchdog**. This is my PoC, my sandbox for testing if "Reasoning Agents" are ready for the real world.

---

## What's This Article About?

This article is a deep dive into building a vertical-specific AI agent. It is not a theoretical overview. It is a builder's log.

I will cover:
1.  **The Reasoning Loop**: How I designed an agent that "thinks" before it answers.
2.  **Tool Integration**: How I gave the agent eyes (Web Search) to see the world.
3.  **The "Watchdog" Architecture**: How I structured the application to be business-centric.
4.  **The Code**: I will share the actual Python code I wrote to make this work.

In my opinion, the difference between a "Chatbot" and an "Agent" is **autonomy** and **reasoning**. A chatbot answers your question. An agent solves your problem. This article is about building the latter.

---

## Tech Stack

For this experiment, I chose a stack that I think balances power with simplicity:

1.  **Phidata**: I chose this purely because I wanted a lightweight framework that treats "Agents" as first-class citizens without the bloat. It handles the memory and tool orchestration beautifully.
2.  **OpenAI GPT-4o**: As per my testing, we need a model with high reasoning capabilities. GPT-4o is currently the gold standard for following complex multi-step instructions.
3.  **DuckDuckGo Search**: I needed a free, reliable way to get real-time news.
4.  **Streamlit**: For the frontend. I wanted a clean dashboard, not a CLI, because visual impact matters.
5.  **Mermaid.js**: For generating the diagrams you see here. I script them in Python because I believe in "Code as Configuration" even for images.

---

## Why Read It?

You should read this if:
1.  You are tired of "Hello World" AI tutorials and want to build something that solves a **real business problem**.
2.  You want to understand how **Reasoning Agents** differ from standard RAG (Retrieval-Augmented Generation) pipelines.
3.  You want to see how I architected a modular agent system that is easy to extend.

I put this way because I believe the best way to learn is to deconstruct a working system. By the end of this, you will have a template you can adapt for financial monitoring, competitor analysis, or any other "Watchdog" use case.

---

## Let's Design

Before I wrote a single line of code, I sat down and sketched the architecture. I didn't want a spaghetti mess of scripts. I wanted a clean flow of data.

![Architecture Diagram](https://raw.githubusercontent.com/aniket-work/autonomous-supply-chain-watchdog/main/images/architecture_diagram.png?v=1)

In my opinion, the most critical part of this design is the **Agent Logic** block. Notice how the "Planner" (Reasoning Engine) sits between the User and the Tools.

1.  **The User** provides a high-level intent (e.g., "Check Lithium supply").
2.  **The Agent** doesn't just search "Lithium". It breaks it down:
    *   "I need to look for recent news."
    *   "I need to filter for 'shortages', 'delays', or 'price spikes'."
    *   "I need to verify the dates of these articles."
3.  **The Tools** fetch the raw data.
4.  **The Agent** synthesis the data into a **Risk Report**.

I designed it this way because raw search results are useless to a business user. They need the *synthesis*.

![Sequence Diagram](https://raw.githubusercontent.com/aniket-work/autonomous-supply-chain-watchdog/main/images/sequence_diagram.png?v=1)

The sequence diagram above illustrates this "Reasoning Loop." It’s not linear. The agent might search, find nothing, refine its search terms, and search again. This "looping" behavior is what makes it intelligent.

---

## Let’s Get Cooking

Now, let's look at the implementation. I broke the project down into three main files: `tools.py`, `agent.py`, and `app.py`.

### 1. The Eyes: Building the Search Tool

First, I needed to give the agent the ability to see the world. I used the `DuckDuckGo` search library wrapped in a Phidata Toolkit.

I wrote this wrapper to specifically target **news**, because for supply chain monitoring, we care about *current events*, not general knowledge.

```python
# supply_chain_watchdog/tools.py

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
                # specifically requesting 'news' results
                ddgs_gen = ddgs.news(query, max_results=max_results)
                for r in ddgs_gen:
                    results.append(r)
        except Exception as e:
            return f"Error searching news: {e}"
        return results
```

**My Logic Here**: I encapsulated the search logic in a class. This makes it modular. If I later decide to switch to `Google SerpAPI` or `Exa.ai`, I just have to update this one file. The agent interaction remains unchanged.

### 2. The Brain: The Reasoning Agent

This is the core. I configured the Phidata Agent with specific instructions to act as a **Risk Analyst**.

I formulated the system prompt very carefully. In my experience, the quality of an agent is 90% determined by its instructions. I told it specifically to assess **Risk Levels** (Low/Medium/High) and provide **Actionable Advice**.

```python
# supply_chain_watchdog/agent.py

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from supply_chain_watchdog.tools import SupplyChainTools
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
            "When received a query, use the `search_news` tool to find the latest relevant information.",
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
```

**Why I did this**: By explicitly instructing the agent to categorize risk levels, I turn unstructured text (news articles) into structured data (Low/Med/High). This is crucial for business dashboards.

### 3. The Face: Streamlit Dashboard

Finally, I built a UI. A console log isn't enough for a PoC I want to impress people with. I used Streamlit because it allows me to build data apps in pure Python.

```python
# supply_chain_watchdog/app.py

import streamlit as st
from supply_chain_watchdog.agent import get_supply_chain_agent

st.set_page_config(page_title="Autonomous Supply Chain Watchdog", page_icon="📦", layout="wide")

st.title("📦 Autonomous Supply Chain Watchdog")

query_input = st.text_input("Enter a commodity, company, or sector:", placeholder="e.g., Lithium")

if st.button("Analyze Risks", type="primary"):
    if query_input:
        with st.status("🔍 Agent is working...", expanded=True) as status:
            agent = get_supply_chain_agent()
            
            # The agent autonomously executes tools and thinks
            response = agent.run(f"Analyze the supply chain risks regarding: {query_input}")
            
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
            
            st.divider()
            st.markdown(response.content)
```

**My Insight**: I used `st.status` to give visual feedback while the agent is "thinking." This improves the user experience significantly, as agentic workflows can sometimes take 10-20 seconds.

---

## Let's Setup

If you want to run this experiment yourself, I have made the setup process extremely simple.

### Step 1: Clone the Repository
Start by cloning the code from my GitHub.

```bash
git clone https://github.com/aniket-work/autonomous-supply-chain-watchdog.git
cd autonomous-supply-chain-watchdog
```

### Step 2: Create a Virtual Environment
In my opinion, you should always keep your dependencies isolated.

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or `venv\Scripts\activate` on Windows
```

### Step 3: Install Dependencies
I have listed all requirements in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Step 4: Configure Keys
You will need an OpenAI API key. Create a `.env` file:

```bash
export OPENAI_API_KEY=sk-proj-...
```

---

## Let's Run

Now for the moment of truth. Run the application:

```bash
streamlit run app.py
```

I tested it with the query **"Cocoa Supply Chain"**.

Here is what happened (behind the scenes):
1.  The Agent recognized "Cocoa" as the commodity.
2.  It generated search queries like *"Cocoa supply chain shortage news 2025"*, *"Ivory Coast cocoa harvest reports"*, *"Cocoa price analysis"*.
3.  It read 5 different articles about weather patterns in West Africa and disease outbreaks affecting trees.
4.  It synthesized this into a report.

**The Output:**
The agent reported a **High Risk** status. It cited "Adverse weather in West Africa" and " swollen shoot disease" as key drivers. It advised strictly monitoring inventory levels and hedging price exposure.

This, to me, was a "wow" moment. The agent successfully navigated from a vague prompt to a specific, actionable business advisory without any human hand-holding.

![Workflow Diagram](https://raw.githubusercontent.com/aniket-work/autonomous-supply-chain-watchdog/main/images/workflow_diagram.png?v=1)

---

## Closing Thoughts

I wrote this code in a few hours, but I think the implications are massive. We are moving away from software that waits for input to software that **proactively** seeks answers.

In my experiment, I found that the quality of the "reasoning" is heavily dependent on the LLM. GPT-4o was excellent. Smaller models struggled to synthesize conflicting news reports.

This **Autonomous Supply Chain Watchdog** is just a PoC, but it demonstrates a clear path toward "Agentic Business Intelligence." Instead of dashboards that show you *what happened*, we will have agents that tell you *what might happen* and *what to do about it*.

I hope you found this breakdown helpful. I plan to extend this with more tools (like stock market API integration) in the future.

If you build something similar, let me know!

---

### Disclaimer

The views and opinions expressed here are solely my own and do not represent the views, positions, or opinions of my employer or any organization I am affiliated with. The content is based on my personal experience and experimentation and may be incomplete or incorrect. Any errors or misinterpretations are unintentional, and I apologize in advance if any statements are misunderstood or misrepresented.

**MOST IMPORTANT**: Always refer to this article as my experiments, my PoCs. It is not real production work or related to what I did in my company projects. It is purely an experimental article.
