from crewai import Agent
from config import get_llm

def create_researcher():
    return Agent(
        role="Supplier Research Specialist",
        goal="Find accurate supplier information for manufacturing needs",
        backstory="Expert in sourcing suppliers and supply chain analysis",
        llm=get_llm(),   # now string ✅
        verbose=True
    )