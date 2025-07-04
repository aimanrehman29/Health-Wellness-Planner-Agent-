from agents import RunContextWrapper, Agent
from datetime import datetime

def log_event(event_name: str, details: str):
    print(f"[{datetime.now()}] {event_name}: {details}")

def on_agent_start(agent: Agent, context_wrapper: RunContextWrapper):
    log_event("Agent Started", f"Agent {agent.name} has started processing.")

def on_agent_end(agent: Agent, context_wrapper: RunContextWrapper):
    log_event("Agent Ended", f"Agent {agent.name} has finished processing.")

def on_tool_start(agent: Agent, tool_name: str, context_wrapper: RunContextWrapper):
    log_event("Tool Started", f"Tool {tool_name} started for agent {agent.name}.")

def on_tool_end(agent: Agent, tool_name: str, context_wrapper: RunContextWrapper):
    log_event("Tool Ended", f"Tool {tool_name} completed for agent {agent.name}.")

def on_handoff(agent: Agent, to_agent_name: str, context_wrapper: RunContextWrapper):
    log_event("Handoff", f"Agent {agent.name} is handing off to {to_agent_name}.")
