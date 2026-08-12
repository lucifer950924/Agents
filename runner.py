from pathlib import Path
import os, time, asyncio
from agents import create_agent

def main():
    TRAINER_PROMPT_DIR = Path(__file__).parent / "agents" / "trainer_agent.txt"
    INFO_COLLECTOR_DIR = Path(__file__).parent / "agents" / "information_collector.txt"
    ORCHESTRATOR_DIR = Path(__file__).parent / "agents" / "orchestrator.txt"

    with open(TRAINER_PROMPT_DIR, "r" , encoding="utf-8") as file:
        trainer = file.read()


    with open(INFO_COLLECTOR_DIR, "r" , encoding="utf-8") as file:
        collector = file.read()

    with open(ORCHESTRATOR_DIR, "r" , encoding="utf-8") as file:
            orchestrator = file.read()


    
    
    

    from typing import TypedDict

    class AgentState(TypedDict):
        question : str
        information : dict
        trained_info : dict
        answer: str

    def collector_agent(state: AgentState):
        print("collector agent working")
        question = state["question"]
        info = create_agent(collector,question)
        return {
            "information" : info
        }

    def trainer_agent(state: AgentState):
        print("trainer agent working")
        info = state["information"]
        trained_info = create_agent(trainer,info)
        return {
            "trained_info" : trained_info
        }     

    def orchestrator_agent_replier(state: AgentState):
        print("replier agent working")
        trained_info = state["trained_info"]

        answer = create_agent(orchestrator,trained_info)

        return {
             "answer" : answer
        }

    from langgraph.graph import StateGraph, START,END

    graph = StateGraph(AgentState)

    graph.add_node("collector_agent",collector_agent)
    graph.add_node("trainer_agent",trainer_agent)
    graph.add_node("orchestrator_agent_replier",orchestrator_agent_replier)

    graph.add_edge(START,"collector_agent")
    graph.add_edge("collector_agent","trainer_agent")
    graph.add_edge('trainer_agent',"orchestrator_agent_replier")
    graph.add_edge("orchestrator_agent_replier",END)

    app = graph.compile()

    print(app.invoke({"question":"Mahatma Gandhi"}))



if __name__ == "__main__":
    main()