import base64
import requests
import os

# Create images directory if not exists
if not os.path.exists("images"):
    os.makedirs("images")

def generate_mermaid_png(name, mermaid_code):
    """
    Generates a PNG from mermaid code using mermaid.ink and saves it.
    """
    print(f"Generating {name}...")
    graphbytes = mermaid_code.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    url = "https://mermaid.ink/img/" + base64_string
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"images/{name}.png", 'wb') as f:
                f.write(response.content)
            print(f"✅ Saved images/{name}.png")
        else:
            print(f"❌ Failed to generate {name}. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error generating {name}: {e}")

# --- DIALGRAM DEFINITIONS ---

title_diagram = """
graph LR
    subgraph Title[Autonomous Supply Chain Watchdog]
        direction TB
        A[<b>Global News Stream</b><br/>Monitor Real-time Data]:::input
        B[<b>AI Reasoning Agent</b><br/>Analyze, Filter, Assess]:::core
        C[<b>Actionable Intelligence</b><br/>Risk Reports & Alerts]:::output
        
        A --> B --> C
    end
    
    classDef input fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef core fill:#fff3e0,stroke:#ff6f00,stroke-width:4px;
    classDef output fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef title fill:#f5f5f5,stroke:#333,stroke-width:2px,font-size:20px;
    
    style Title fill:#ffffff,stroke:#333,stroke-width:2px
"""

architecture_diagram = """
flowchart TB
    User[User / Analyst] -->|Topic Query| UI[Streamlit Dashboard]
    UI -->|Input| Agent[Phidata Agent]
    
    subgraph AgentLogic [Supply Chain Watchdog Agent]
        Planner[Reasoning Engine]
        Tools[Toolkit]
    end
    
    Agent --> Planner
    Planner -->|Search Request| Tools
    Tools -->|DuckDuckGo| Web((The Internet))
    Web -->|News Snippets| Tools
    Tools -->|Context| Planner
    Planner -->|Risk Assessment| Agent
    Agent -->|Final Report| UI
    
    style User fill:#f9f9f9,stroke:#333
    style UI fill:#e3f2fd,stroke:#2196f3
    style AgentLogic fill:#fff3e0,stroke:#ff9800
    style Web fill:#f3e5f5,stroke:#9c27b0
"""

sequence_diagram = """
sequenceDiagram
    actor U as User
    participant App as Streamlit App
    participant Ag as AI Agent
    participant Tool as Search Tool
    
    U->>App: Enter Commodity (e.g., "Cobalt")
    App->>Ag: Run Analysis("Cobalt")
    loop Reasoning Loop
        Ag->>Ag: Plan Search Strategy
        Ag->>Tool: search_news("Cobalt supply chain")
        Tool-->>Ag: Returns Article Snippets
        Ag->>Ag: Analyze Service Risks
    end
    Ag-->>App: Return Risk Report (High/Med/Low)
    App-->>U: Display Report & Actions
"""

workflow_diagram = """
graph TD
    start((Start)) --> input[Input Commodity]
    input --> search[Search Live News]
    search --> analyze{Analyze Impact}
    
    analyze -->|Disruption Found| assess_risk[Assess Risk Level]
    analyze -->|No Major News| low_risk[Mark as Low Risk]
    
    assess_risk -->|Critical| high[High Risk Alert]
    assess_risk -->|Moderate| med[Medium Risk Alert]
    
    high --> report[Generate Report]
    med --> report
    low_risk --> report
    
    report --> stop((End))
    
    style start fill:#cfc,stroke:#333
    style stop fill:#cfc,stroke:#333
    style high fill:#ffcdd2,stroke:#f44336
    style med fill:#fff9c4,stroke:#fbc02d
    style low_risk fill:#c8e6c9,stroke:#4caf50
"""

# Experiment: Using mermaid.ink to generate images
if __name__ == "__main__":
    generate_mermaid_png("title_diagram", title_diagram)
    generate_mermaid_png("architecture_diagram", architecture_diagram)
    generate_mermaid_png("sequence_diagram", sequence_diagram)
    generate_mermaid_png("workflow_diagram", workflow_diagram)
