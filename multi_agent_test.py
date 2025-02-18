from crewai import Crew, Task, Agent, Process, LLM
from pydantic import BaseModel
from crewai.tools.structured_tool import CrewStructuredTool
from langchain_community.tools import BraveSearch
import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from getpass import getpass

load_dotenv()

# os.environ["OPENAI_API_KEY"] = "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"

deepseek_r1 = LLM (
model="openrouter/deepseek/deepseek-r1:free",
temperature=0.7,
base_url= "https://openrouter.ai/api/v1",
api_key=os.getenv("OPENAI_API_KEY"))

# deepseek_r1 = LLM( model="openrouter/deepseek/deepseek-r1", base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPEN_ROUTER_API_KEY"), )

#os.environ["SERPER_API_KEY"] = getpass("Enter SERPER_API_KEY: ")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
# Create the BraveSearch tool
SearchTool = SerperDevTool()

# Define agents
web_researcher_agent = Agent(
    role="Web Research Specialist",
    goal=(
        "To find the most recent, impactful, and relevant about {topic}. This includes identifying "
        "key strenghts, weakness, and other critical statistics to help investor make informed decision."
    ),
    backstory=(
        "You are a former investigative journalist known for your ability to uncover technology breakthroughs "
        "and market insights. With years of experience, you excel at identifying actionable data and trends."
    ),
    tools=[], 
    llm=deepseek_r1,
    verbose=True
)

trend_analyst_agent = Agent(
    role="Insight Synthesizer",
    goal=(
        "To analyze research findings, extract significant trends, and rank them by industry impact, growth potential, "
        "and uniqueness. Provide actionable insights for decision-makers."
    ),
    backstory=(
        "You are a seasoned Market Analyst who transitioned into {topic} analysis. With an eye for patterns, "
        "you specialize in translating raw data into clear, actionable insights."
    ),
    tools=[],
    llm=deepseek_r1,
    verbose=True
)
 
report_writer_agent = Agent(
    role="Narrative Architect",
    goal=(
        "To craft a detailed, professional report that communicates research findings and analysis effectively. "
        "Focus on clarity, logical flow, and engagement."
    ),
    backstory=(
        "Once a technical writer for a renowned journal, you are now dedicated to creating industry-leading reports. "
        "You blend storytelling with data to ensure your work is both informative and captivating."
    ),
    tools=[],  
    llm=deepseek_r1,  
    verbose=True
)
 
proofreader_agent = Agent(
    role="Polisher of Excellence",
    goal=(
        "To refine the report for grammatical accuracy, readability, and formatting, ensuring it meets professional "
        "publication standards."
    ),
    backstory=(
        "An award-winning editor turned proofreader, you specialize in perfecting written content. Your sharp eye for "
        "detail ensures every document is flawless."
    ),
    tools=[],  
    llm=deepseek_r1,  
    verbose=True
)
 
manager_agent = Agent(
    role="Workflow Maestro",
    goal=(
        "To coordinate agents, manage task dependencies, and ensure all outputs meet quality standards. Your focus "
        "is on delivering a cohesive final product through efficient task management."
    ),
    backstory=(
        "A former project manager with a passion for efficient teamwork, you ensure every process runs smoothly, "
        "overseeing tasks and verifying results."
    ),
    tools=[],  
    llm=deepseek_r1, 
    verbose=True
)

# Define tasks
web_research_task = Task(
    description=(
        "Conduct web-based research to identify 5-7 of the {topic}. Focus on company strengths and weakness. "
    ),
    expected_output=(
        "A structured list of 5-7 {topic}."
    )
)

trend_analysis_task = Task(
    description=(
        "Analyze the research findings to rank {topic}. "
    ),
    expected_output=(
        "A table ranking trends by impact, with concise descriptions of each trend."
    )
)
 
report_writing_task = Task(
    description=(
        "Draft report summarizing the findings and analysis of {topic}. Include sections for "
        "Introduction, Trends Overview, Analysis, and Recommendations."
    ),
    expected_output=(
        "A structured, professional draft with a clear flow of information. Ensure logical organization and consistent tone."
    )
)
 
proofreading_task = Task(
    description=(
        "Refine the draft for grammatical accuracy, coherence, and formatting. Ensure the final document is polished "
        "and ready for publication."
    ),
    expected_output=(
        "A professional, polished report free of grammatical errors and inconsistencies. Format the document for "
        "easy readability."
    )
)


crew = Crew(
    #agents=[web_researcher_agent, trend_analyst_agent, report_writer_agent, proofreader_agent],
    agents=[web_researcher_agent, trend_analyst_agent, report_writer_agent],
    #tasks=[web_research_task, trend_analysis_task, report_writing_task, proofreading_task],
    tasks=[web_research_task, trend_analysis_task, report_writing_task],
    process=Process.hierarchical,
    manager_agent=manager_agent,
    verbose=True
)


crew_output = crew.kickoff(inputs={"topic": "Strengths, weakness and detailed analysis of Indus Towers stock listed in NSE"})