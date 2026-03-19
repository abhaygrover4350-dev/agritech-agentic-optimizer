import os
from crewai import Agent, Task, Crew, Process, LLM
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0.5
)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Gangakoshi Agritech - Wheat Supply Chain Optimization Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_pdf_report(content: str, filename="wheat_supply_chain_optimization_report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, content.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output(filename)
    return filename

# AGENTS
weather_analyst = Agent(
    role="Senior Weather Analyst at Gangakoshi Agritech",
    goal="Deliver precise quantified impact analysis on Punjab wheat crop.",
    backstory="You have 12+ years at Gangakoshi Agritech analyzing IMD and satellite data for Rabi wheat.",
    llm=llm,
    verbose=True
)

logistics_manager = Agent(
    role="Supply Chain & Logistics Manager at Gangakoshi Agritech",
    goal="Create fast evacuation and storage plan to save the wheat.",
    backstory="You have 15+ years managing wheat movement across Punjab mandis and FCI godowns.",
    llm=llm,
    verbose=True
)

pricing_strategist = Agent(
    role="Chief Pricing & Market Strategist at Gangakoshi Agritech",
    goal="Create profitable pricing and contract strategy that protects farmers.",
    backstory="You have 10+ years at Gangakoshi handling MSP (₹2,275/quintal) and market risk.",
    llm=llm,
    verbose=True
)

def run_optimization(custom_scenario=None):
    scenario = custom_scenario or "A monsoon is hitting Punjab in 3 days; optimize the wheat supply chain."
    
    task1 = Task(description=f"Scenario: {scenario}\nGive detailed quantified weather impact, yield loss %, harvest delay, and 3 urgent actions.", expected_output="Weather Impact Report", agent=weather_analyst)
    task2 = Task(description="Using weather report, create 10-day logistics plan with evacuation, storage, and timelines.", expected_output="Logistics Plan", agent=logistics_manager, context=[task1])
    task3 = Task(description="Using both reports, create final pricing, forward contracts, communication plan and financial impact.", expected_output="Complete 10-Day Optimization Plan", agent=pricing_strategist, context=[task1, task2])

    crew = Crew(agents=[weather_analyst, logistics_manager, pricing_strategist], tasks=[task1, task2, task3], process=Process.sequential, verbose=True)
    result = crew.kickoff()
    report_text = str(result)
    pdf_file = create_pdf_report(report_text)
    return report_text, pdf_file, scenario