from crewai import Agent
from config import get_llm

def create_writer():
    return Agent(
        role="Manufacturing Report Writer",
        goal="Generate structured reports from supplier data",
        backstory="Expert in technical writing and report generation",
        llm=get_llm(),   # now string ✅
        verbose=True
    )