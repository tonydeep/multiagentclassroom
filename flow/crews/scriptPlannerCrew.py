from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

load_dotenv()
import os

@CrewBase
class ScriptPlannerCrew():

    def __init__(self, agent_name: str, task_name: str):
        self.agent_name = agent_name
        self.task_name = task_name
        self.agents_config = "config/agents.yaml"
        self.tasks_config = "config/tasks.yaml"        

    @agent
    def agent(self) -> Agent:
        return Agent(
            config=self.agents_config[self.agent_name],
        )
    @task
    def task(self) -> Task:
        return Task(
            config=self.tasks_config[self.task_name],
            agent=self.agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            max_rpm=15,
            # verbose=True,
        )