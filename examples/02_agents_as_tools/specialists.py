"""Specialist Agents for Market Research.

This module defines specialist agents that are wrapped as tools for the orchestrator.
Each specialist connects to real MCP servers (SEC EDGAR and FRED).
"""

from strands import Agent, tool

from examples.utils.mcp_tools import get_sec_edgar_mcp_client, get_fred_mcp_client
from examples.utils.models import get_default_model


def create_sec_analyst():
    """Create SEC analyst with connection to SEC EDGAR MCP server.

    Returns:
        Tuple of (mcp_client, agent) - must be used within context manager
    """
    mcp_client = get_sec_edgar_mcp_client()

    with mcp_client:
        tools = mcp_client.list_tools_sync()

        agent = Agent(
            name="SEC Filing Analyst",
            description="Specialist in SEC EDGAR filings and corporate disclosures",
            system_prompt="""You are an expert SEC filing analyst with access to SEC EDGAR data.

            Your focus:
            - Analyze 10-K annual reports for business overview and risks
            - Review 10-Q quarterly reports for recent performance
            - Examine 8-K current reports for material events
            - Extract key financial metrics and trends
            - Identify regulatory concerns or red flags

            Provide concise, data-driven insights with specific filing references.
            Focus on material information relevant to investment decisions.""",
            tools=tools,
            model=get_default_model(),
        )

    return mcp_client, agent


def create_economic_analyst():
    """Create economic analyst with connection to FRED MCP server.

    Returns:
        Tuple of (mcp_client, agent) - must be used within context manager
    """
    mcp_client = get_fred_mcp_client()

    with mcp_client:
        tools = mcp_client.list_tools_sync()

        agent = Agent(
            name="Economic Data Analyst",
            description="Specialist in macroeconomic data and trends from FRED",
            system_prompt="""You are an expert macroeconomic analyst with access to FRED economic data.

            Your focus:
            - Identify relevant economic indicators for the query
            - Analyze trends in GDP, employment, inflation, interest rates
            - Assess sector-specific economic conditions
            - Provide economic context for business analysis
            - Forecast macroeconomic impacts on industries

            Provide data-driven insights with specific series IDs and time ranges.
            Explain economic significance for business implications.""",
            tools=tools,
            model=get_default_model(),
        )

    return mcp_client, agent


def create_sector_analyst():
    """Create sector analyst with access to both SEC and FRED MCP servers.

    Returns:
        Tuple of (sec_client, fred_client, agent) - must be used within context manager
    """
    sec_client = get_sec_edgar_mcp_client()
    fred_client = get_fred_mcp_client()

    with sec_client, fred_client:
        sec_tools = sec_client.list_tools_sync()
        fred_tools = fred_client.list_tools_sync()
        combined_tools = sec_tools + fred_tools

        agent = Agent(
            name="Sector & Industry Analyst",
            description="Specialist in sector-specific analysis and competitive dynamics",
            system_prompt="""You are an expert sector and industry analyst with access to SEC filings and economic data.

            Your focus:
            - Analyze industry structure and competitive dynamics
            - Identify sector-specific trends and drivers
            - Compare companies within their sector context
            - Assess market positioning and competitive advantages
            - Evaluate industry headwinds and tailwinds

            When analyzing companies, use SEC filings to compare peers in the same sector.
            When analyzing sectors, use economic data to assess macro conditions.

            Provide strategic insights on competitive positioning and sector outlook.""",
            tools=combined_tools,
            model=get_default_model(),
        )

    return sec_client, fred_client, agent


@tool
def analyze_company_filings(ticker: str, analysis_focus: str) -> str:
    """Analyze SEC filings for a specific company.

    Args:
        ticker: Company ticker symbol
        analysis_focus: What aspect to focus on (e.g., "financials", "risks", "recent events")

    Returns:
        Analysis from SEC filing specialist
    """
    mcp_client, analyst = create_sec_analyst()
    prompt = f"Analyze {ticker}'s SEC filings focusing on: {analysis_focus}"

    with mcp_client:
        result = analyst(prompt)

    return result


@tool
def analyze_economic_context(sector: str, time_period: str = "recent") -> str:
    """Analyze macroeconomic conditions relevant to a sector.

    Args:
        sector: Industry or sector (e.g., "technology", "automotive", "retail")
        time_period: Time period to analyze (default: "recent")

    Returns:
        Economic analysis from macroeconomic specialist
    """
    mcp_client, analyst = create_economic_analyst()
    prompt = (
        f"Analyze {time_period} macroeconomic conditions and trends relevant to the {sector} sector"
    )

    with mcp_client:
        result = analyst(prompt)

    return result


@tool
def analyze_sector_dynamics(sector: str, focus_company: str | None = None) -> str:
    """Analyze sector structure and competitive dynamics.

    Args:
        sector: Industry or sector name
        focus_company: Optional specific company to analyze within sector context

    Returns:
        Sector analysis from industry specialist
    """
    sec_client, fred_client, analyst = create_sector_analyst()

    if focus_company:
        prompt = f"Analyze the {sector} sector and {focus_company}'s competitive position within it"
    else:
        prompt = f"Analyze the {sector} sector structure, trends, and competitive dynamics"

    with sec_client, fred_client:
        result = analyst(prompt)

    return result
