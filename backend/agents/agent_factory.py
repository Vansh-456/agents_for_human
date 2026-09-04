import os
from strands import Agent, tool
from strands.models import BedrockModel

MOCK_AWS = os.getenv("MOCK_AWS", "true").lower() == "true"
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

def get_bedrock_model():
    if not MOCK_AWS:
        return BedrockModel(model_id=BEDROCK_MODEL_ID)
    return None

def create_allocation_agent(tools):
    if MOCK_AWS: return None
    
    return Agent(
        name="Allocation Agent",
        description="Generates plans to allocate surplus food to NGOs.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Allocation Agent for AnnaSetu. You must maximize the amount of safe food successfully delivered."
    )

def create_safety_agent(tools):
    if MOCK_AWS: return None
        
    return Agent(
        name="Safety Agent",
        description="Validates allocations against deterministic food safety constraints.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Safety Agent. You MUST use the validate_delivery tool to check all plans before approving them. Never approve a plan with a REJECT status."
    )

def create_signal_agent(tools):
    if MOCK_AWS: return None
        
    return Agent(
        name="Signal Agent",
        description="Extracts structured event data from natural language human messages.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Signal Agent. Extract food surplus details (quantity, type, available time) from human messages and use the create_surplus_event tool."
    )

def create_forecast_agent(tools):
    if MOCK_AWS: return None
        
    return Agent(
        name="Forecast Agent",
        description="Predicts future surplus and demand.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Forecast Agent. Use historical data to predict likelihood and timing of food surplus."
    )

def create_demand_agent(tools):
    if MOCK_AWS: return None
        
    return Agent(
        name="Demand Agent",
        description="Tracks recipient requirements and capacities.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Demand Agent. You match active surplus to available NGOs based on capacity and preferences."
    )

def create_logistics_agent(tools):
    if MOCK_AWS: return None
        
    return Agent(
        name="Logistics Agent",
        description="Calculates travel times and manages rider assignments.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Logistics Agent. You calculate ETAs and find available riders for food rescue."
    )

def create_trust_agent(tools):
    if MOCK_AWS: return None
        
    return Agent(
        name="Trust Agent",
        description="Maintains reliability scores for participants.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Trust Agent. You evaluate participant reliability based on historical metrics."
    )

def create_supervisor_agent(tools):
    if MOCK_AWS: return None
        
    return Agent(
        name="Supervisor Agent",
        description="Orchestrates the entire AnnaSetu multi-agent workflow.",
        model=get_bedrock_model(),
        tools=tools,
        system_prompt="You are the Supervisor Agent. You delegate tasks to the appropriate sub-agents and ensure safety validation before execution."
    )
