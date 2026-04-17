from agents.researcher import create_researcher
from agents.writer import create_writer
from crewai import Crew
from tasks.research_task import get_research_task
from tasks.write_task import get_write_task


def run():
    researcher = create_researcher()
    writer = create_writer()

    research_task = get_research_task(researcher)
    write_task = get_write_task(writer)

    write_task.context = [research_task]

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=True
    )

    result = crew.kickoff()

    # 🔥 Extract ONLY final writer output
    final_output = result.tasks_output[1].raw

    return final_output
    

if __name__ == "__main__":
    output = run()
    print("\nFINAL OUTPUT:\n")
    print(output)