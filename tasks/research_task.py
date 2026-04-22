from crewai import Task


def get_research_task(agent, industry="Aluminum", location="India"):
    return Task(
        description=(
            f"Find top 3 {industry} suppliers in {location}. "
            "Return output ONLY in JSON format like:\n\n"
            '{"suppliers": [{"name": "...", "location": "...", "price_range": "...", "lead_time": "..."}]}'
        ),
        agent=agent,
        expected_output="Strict JSON with supplier details"
    )