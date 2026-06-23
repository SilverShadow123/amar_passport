from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai_tools import SerperDevTool
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


project_root = Path(__file__).resolve().parent.parent.parent
passport_knowledge = JSONKnowledgeSource(
    file_paths=[project_root / "knowledge" / "passport_db.json"],
)

search_tool = SerperDevTool()

custom_llm = LLM(
    model="openrouter/openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.3,
)


@CrewBase
class AmarPassport:
    """AmarPassport crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def police_guardian(self) -> Agent:
        return Agent(
            config=self.agents_config["police_guardian"],
            tools=[search_tool],
            llm=custom_llm,
            verbose=True,
        )

    @agent
    def chancellor_of_the_exchequer(self) -> Agent:
        return Agent(
            config=self.agents_config["chancellor_of_the_exchequer"],
            tools=[search_tool],
            llm=custom_llm,
            verbose=True,
        )

    @agent
    def document_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["document_architect"],
            llm=custom_llm,
            verbose=True,
        )

    @agent
    def passport_readiness_officer(self) -> Agent:
        return Agent(
            config=self.agents_config["passport_readiness_officer"],
            llm=custom_llm,
            verbose=True,
        )

    @task
    def eligibility_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["eligibility_analysis_task"],
        )

    @task
    def fee_calculation_task(self) -> Task:
        return Task(
            config=self.tasks_config["fee_calculation_task"],
        )

    @task
    def document_checklist_task(self) -> Task:
        return Task(
            config=self.tasks_config["document_checklist_task"],
        )

    @task
    def passport_readiness_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["passport_readiness_report_task"],
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AmarPassport crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[passport_knowledge],
            embedder={
                "provider": "sentence-transformer",
                "config": {},
            },
        )
