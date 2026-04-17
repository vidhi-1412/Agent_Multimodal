from crewai import Task

def get_research_task(agent):
    return Task(
        description=(
            "Find top 3 aluminum suppliers in India. "
            "Return output ONLY in JSON format like:\n\n"
            "{\n"
            '  "suppliers": [\n'
            "    {\n"
            '      "name": "...",\n'
            '      "location": "...",\n'
            '      "price_range": "...",\n'
            '      "lead_time": "..."\n'
            "    }\n"
            "  ]\n"
            "}"
        ),
        agent=agent,
        expected_output="Strict JSON with supplier details"
    )