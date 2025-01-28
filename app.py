from datetime import datetime
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from research_agent import ResearchAgent

# Step 1: Define the Tool for Dynamic Crew Execution
@tool
def kickoff_crew(crew_name: str, topic: str, current_date: str) -> str:
    """
    Executes a specified crew dynamically based on its name.

    Parameters:
        crew_name (str): The name of the crew to execute. 
                         Options are 'research_crew' or 'content_crew'.
        topic (str): The topic on which the workflow should focus.
        current_date (str): The current date in 'YYYY-MM-DD' format.

    Returns:
        str: The result of the executed crew.
    """
    if crew_name == "research_crew":
        # Define Research Crew
        researcher = ResearchAgent.research_agent(topic)
        research_task = ResearchAgent.research_task(topic)
        analysis_task = ResearchAgent.analysis_task(topic)
        
        research_crew = Crew(
            agents=[researcher],
            tasks=[research_task, analysis_task],
            process=Process.sequential
        )
        
        # Execute the Research Crew
        result = research_crew.kickoff(inputs={'topic': topic})
        return f"Research Process Result:\n{result}"

    elif crew_name == "content_crew":
        # Define Content Crew
        writer = Agent(
            role="Writer",
            goal="Write and edit high-quality articles.",
            verbose=True,
            memory=True,
            backstory="A creative writer who excels at crafting engaging and informative articles."
        )
        
        writing_task = Task(
            description=f"Write a compelling article on '{topic}' using data available as of {current_date}.",
            expected_output="An article in markdown format about {topic}.",
            agent=writer
        )
        
        editing_task = Task(
            description="Review and edit the article for clarity and formatting.",
            expected_output="A polished final article about {topic}.",
            agent=writer
        )
        
        content_crew = Crew(
            agents=[writer],
            tasks=[writing_task, editing_task],
            process=Process.sequential
        )
        
        # Execute the Content Crew
        result = content_crew.kickoff(inputs={'topic': topic})
        return f"Content Process Result:\n{result}"

    else:
        return f"No crew found with name: {crew_name}"


# Step 2: Define the Decision-Maker Agent
decision_maker = Agent(
    role="Decision Maker",
    goal="Analyze user queries and decide which workflow to execute dynamically.",
    verbose=True,
    memory=False,
    tools=[kickoff_crew],
    backstory="A skilled decision-maker capable of dynamically triggering workflows."
)

decision_task = Task(
    description=(
        "Analyze the user query: '{query}'. Based on the query, determine the appropriate workflow "
        "(e.g., 'research_crew' or 'content_crew'). Use the 'kickoff_crew' tool to execute the selected crew dynamically."
    ),
    expected_output="The workflow is executed dynamically by calling the 'kickoff_crew' tool.",
    agent=decision_maker
)

# Step 3: Define the Main Crew
main_crew = Crew(
    agents=[decision_maker],
    tasks=[decision_task],
    process=Process.sequential
)

# Step 4: Execute the Workflow
def execute_dynamic_workflow(query, topic):
    # Get today's date
    current_date = datetime.today().strftime('%Y-%m-%d')
    
    # Run the main crew, which triggers the appropriate sub-Crew via the tool
    result = main_crew.kickoff(inputs={'query': query, 'topic': topic, 'current_date': current_date})
    print(result)

# Example Execution
user_query = "I need insights into AI trends."  # This will trigger the research crew
topic = "AI in healthcare"
execute_dynamic_workflow(user_query, topic)

user_query = "Write an article about AI."  # This will trigger the content crew
topic = "AI in healthcare"
execute_dynamic_workflow(user_query, topic)
