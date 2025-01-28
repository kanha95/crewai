from crewai import Agent, Task, Crew, Process
import yaml
class ResearchAgent:
    def __init__(self, name, goal, verbose=False, memory=False, backstory=None):
        self.name = name
        self.goal = goal
        self.verbose = verbose
        self.memory = memory
        self.backstory = backstory
    
    def research_agent(self, topic):
        with open('config/agents.yaml', 'r') as file:
            agents = yaml.safe_load(file)
        result =  Agent(
            role=agents["researcher"]["role"],
            goal=agents["researcher"]["goal"],
            verbose=agents["researcher"]["verbose"],
            memory=agents["researcher"]["memory"],
            backstory=agents["researcher"]["backstory"]
        )
        return result
    

    def research_task(self, topic):
        with open('config/tasks.yaml', 'r') as file:
            tasks = yaml.safe_load(file)
        task = Task(
            description=tasks["research_task"]["description"],
            expected_output=tasks["research_task"]["expected_output"],
            agent=tasks["research_task"]["agent"]
        )
        return task
    
    def analysis_task(self, topic):
        with open('config/tasks.yaml', 'r') as file:
            tasks = yaml.safe_load(file)
        task = Task(
            description=tasks["analysis_task"]["description"],
            expected_output=tasks["analysis_task"]["expected_output"],
            agent=tasks["analysis_task"]["agent"]
        )
        return task
