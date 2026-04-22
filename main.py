from agents.researcher import create_researcher
from agents.writer import create_writer
from crewai import Crew
from tasks.research_task import get_research_task
from tasks.write_task import get_write_task
from memory.vector_store import store_result, search_similar


def run(query="Find top 3 aluminum suppliers in India", industry="Aluminum", location="India"):
    researcher = create_researcher()
    writer = create_writer()

    research_task = get_research_task(researcher, industry=industry, location=location)
    write_task = get_write_task(writer)

    write_task.context = [research_task]

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=True
    )

    result = crew.kickoff()
    final_output = result.tasks_output[1].raw

    # Save to ChromaDB
    store_result(
        query=query,
        result=final_output,
        metadata={"industry": industry, "location": location}
    )

    return final_output


if __name__ == "__main__":
    output = run()
    print("\nFINAL OUTPUT:\n")
    print(output)