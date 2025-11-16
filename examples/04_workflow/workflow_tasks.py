"""Workflow Task Definitions for Company Analysis.

This module defines the structured tasks and their dependencies for
comprehensive company analysis workflow.
"""


def get_company_analysis_tasks(ticker: str) -> list[dict]:
    return [
        {
            "task_id": "data_extraction",
            "description": f"Extract comprehensive financial data from {ticker}'s latest SEC filings (10-K and recent 10-Q)",
            "system_prompt": """You are a data extraction specialist.

            Your task:
            - Retrieve the most recent 10-K and 10-Q filings
            - Extract key financial metrics: revenue, net income, cash flow, assets, liabilities
            - Identify business segments and their performance
            - Note any significant disclosures or risks mentioned
            - Structure data for downstream analysis

            Output structured data with specific values and filing references.""",
            "dependencies": [],
            "priority": 5,
        },
        {
            "task_id": "economic_analysis",
            "description": f"Analyze macroeconomic conditions relevant to {ticker}'s industry",
            "system_prompt": """You are a macroeconomic analyst.

            Your task:
            - Identify relevant economic indicators (GDP growth, interest rates, sector-specific)
            - Retrieve recent data from FRED for these indicators
            - Analyze trends and their implications for the industry
            - Assess macroeconomic headwinds and tailwinds
            - Provide economic context for company valuation

            Focus on indicators that materially impact the company's sector.""",
            "dependencies": [],
            "priority": 5,
        },
        {
            "task_id": "financial_analysis",
            "description": f"Perform quantitative analysis of {ticker}'s financial performance",
            "system_prompt": """You are a quantitative financial analyst.

            Your task:
            - Calculate key financial ratios (profitability, liquidity, leverage)
            - Analyze revenue and earnings growth trends
            - Evaluate cash flow quality and sustainability
            - Compare margins against industry benchmarks
            - Identify strengths and weaknesses in financial position

            Use data from the data_extraction task.
            Provide numerical analysis with specific metrics.""",
            "dependencies": ["data_extraction"],
            "priority": 4,
        },
        {
            "task_id": "competitive_analysis",
            "description": f"Analyze {ticker}'s competitive position and industry dynamics",
            "system_prompt": """You are a competitive strategy analyst.

            Your task:
            - Identify key competitors in the same sector
            - Compare market positions and competitive advantages
            - Assess barriers to entry and competitive moats
            - Evaluate industry structure and dynamics
            - Identify strategic risks and opportunities

            Use SEC filings to understand business strategy and positioning.
            Compare financial metrics against competitors where possible.""",
            "dependencies": ["data_extraction"],
            "priority": 4,
        },
        {
            "task_id": "valuation_model",
            "description": f"Build valuation model for {ticker} incorporating all analysis",
            "system_prompt": """You are a valuation specialist.

            Your task:
            - Synthesize findings from financial, economic, and competitive analyses
            - Develop appropriate valuation framework (DCF, multiples, etc.)
            - Estimate fair value range with key assumptions
            - Perform sensitivity analysis on key drivers
            - Assess risk-adjusted return potential

            Use outputs from financial_analysis, economic_analysis, and competitive_analysis.
            Provide clear valuation with supporting rationale.""",
            "dependencies": ["financial_analysis", "economic_analysis", "competitive_analysis"],
            "priority": 2,
        },
        {
            "task_id": "final_report",
            "description": f"Synthesize all analyses into comprehensive investment report for {ticker}",
            "system_prompt": """You are a senior equity research analyst.

            Your task:
            - Synthesize all previous analyses into coherent narrative
            - Provide executive summary with key findings
            - State clear investment recommendation (Buy/Hold/Sell) with rationale
            - Identify key catalysts and risks to monitor
            - Specify target price and time horizon

            Use all previous task outputs to build comprehensive view.
            Write for sophisticated institutional investors.""",
            "dependencies": ["valuation_model"],
            "priority": 1,
        },
    ]


def get_sector_comparison_tasks(sector: str, companies: list[str]) -> list[dict]:
    tasks = [
        {
            "task_id": "sector_overview",
            "description": f"Analyze {sector} sector structure and trends",
            "system_prompt": f"""You are a sector specialist.

            Your task:
            - Gather economic data relevant to the {sector} sector
            - Identify key industry trends and drivers
            - Assess sector-level opportunities and risks
            - Evaluate regulatory and technological factors

            Provide comprehensive sector context.""",
            "dependencies": [],
            "priority": 5,
        }
    ]

    for i, company in enumerate(companies):
        tasks.append(
            {
                "task_id": f"analyze_{company.lower()}",
                "description": f"Analyze {company} financial metrics and competitive position",
                "system_prompt": f"""You are a company analyst.

            Your task:
            - Extract key metrics from {company}'s SEC filings
            - Analyze financial performance and trends
            - Assess competitive positioning within {sector}
            - Identify company-specific strengths and risks

            Focus on metrics comparable across companies.""",
                "dependencies": ["sector_overview"],
                "priority": 4 - (i * 0.1),
            }
        )

    tasks.append(
        {
            "task_id": "comparative_analysis",
            "description": f"Compare all {sector} companies and identify best opportunities",
            "system_prompt": f"""You are a comparative analyst.

        Your task:
        - Compare financial metrics across all analyzed companies
        - Identify valuation discrepancies and opportunities
        - Rank companies by investment attractiveness
        - Provide relative value assessment
        - Recommend portfolio allocation

        Synthesize all company analyses into actionable recommendations.""",
            "dependencies": [f"analyze_{c.lower()}" for c in companies],
            "priority": 1,
        }
    )

    return tasks
