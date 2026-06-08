from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import TavilySearchTool,SerperDevTool
from research.models import ResearchInput, ResearchOutput
from datetime import datetime
import os 

@CrewBase
class ResearchAgentCrew():
    """Research Agent Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config  = 'config/tasks.yaml'

    def __init__(self):
        self.search_tool = TavilySearchTool()
        

        # Groq LLM
        # self.llm = LLM(
        #     model="groq/llama-3.3-70b-versatile",
        #     api_key=os.getenv("GROQ_API_KEY"),
        #      base_url="https://api.groq.com/openai/v1",
        #     temperature=0.7,
        # )

        self.llm = LLM(
            model="ollama/gpt-oss:20b-cloud",
            base_url="http://localhost:11434"
        )

    # ─────────────────────────────
    # AGENTS
    # ─────────────────────────────

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[self.search_tool],
            llm = self.llm, 
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            llm = self.llm, 
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            llm=self.llm ,
            verbose=True
        )

    # ─────────────────────────────
    # TASKS
    # ─────────────────────────────

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'],
        )

    @task
    def write_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_task'],
            output_file='outputs/reports/report.md'
        )

    # ─────────────────────────────
    # CREW
    # ─────────────────────────────

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.researcher(),
                self.analyst(),
                self.writer()
            ],
            tasks=[
                self.research_task(),
                self.analysis_task(),
                self.write_task()
            ],
            process=Process.sequential,
            verbose=True,
            cache=False
        )

  # ─────────────────────────────
  # MAIN RUN FUNCTION
  # ─────────────────────────────

    def run_research(self, topic: str, depth: str = "detailed") -> ResearchOutput:
        try:
            validated_input = ResearchInput(topic=topic, depth=depth)
        except Exception as e:
            return ResearchOutput(
                topic=topic,
                report="",
                status="error",
                error_message=f"Input validation failed: {str(e)}"
            )

        try:
            result = self.crew().kickoff(
                inputs={"topic": validated_input.topic}
            )

            report_content = result.raw if hasattr(result, "raw") else str(result)
            word_count = len(report_content.split())

            return ResearchOutput(
                topic=validated_input.topic,
                report=report_content,
                status="success",
                word_count=word_count
            )

        except Exception as e:
            return ResearchOutput(
                topic=topic,
                report="",
                status="error",
                error_message=f"Research failed: {str(e)}"
            )