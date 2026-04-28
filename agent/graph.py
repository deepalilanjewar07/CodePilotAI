from langgraph.graph import StateGraph
from langgraph.constants import END

from agent.agents.database_agent import database_agent
from agent.agents.planner_agent import planner_agent
from agent.agents.architect_agent import architect_agent
from agent.agents.backend_agent import backend_agent
from agent.agents.frontend_agent import frontend_agent
from agent.agents.integration_agent import integration_agent

from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq

# ✅ Load env once
load_dotenv()

# ✅ Create ONE shared LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ✅ Build graph
graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("database", database_agent)
graph.add_node("backend", backend_agent)
graph.add_node("frontend", frontend_agent)
graph.add_node("integration", integration_agent)

graph.set_entry_point("planner")

graph.add_edge("planner", "architect")
graph.add_edge("architect", "database")
graph.add_edge("database", "backend")
graph.add_edge("backend", "frontend")

graph.add_conditional_edges(
    "frontend",
    lambda s: "integration" if s.get("status") == "DONE" else "frontend",
    {
        "integration": "integration",
        "frontend": "frontend"
    }
)

graph.add_edge("integration", END)

agent = graph.compile()


# ✅ RUN ONLY WHEN EXECUTED DIRECTLY
if __name__ == "__main__":
    result = agent.invoke(
        {
            "user_prompt": "Build a full stack photo gallery app",
            "llm": llm
        },
        {"recursion_limit": 100}
    )

    print("\n✅ FINAL RESULT:\n", result)