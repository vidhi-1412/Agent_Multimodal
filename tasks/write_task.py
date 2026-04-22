from crewai import Task


def get_write_task(agent):
    return Task(
        description=(
            "Using the supplier JSON data provided, create a structured report:\n"
            "1. List suppliers\n"
            "2. Compare pricing\n"
            "3. Recommend best option"
        ),
        agent=agent,
        expected_output="Well-formatted manufacturing report"
    )