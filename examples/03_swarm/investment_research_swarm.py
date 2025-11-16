#!/usr/bin/env python3
"""Investment Research Swarm Example.

This example demonstrates the Swarm pattern where specialized agents collaborate
autonomously to perform comprehensive investment research using real MCP servers.
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from strands.multiagent import Swarm
from strands import Agent

from examples.utils.config import Config
from examples.utils.models import get_default_model
from examples.utils.mcp_tools import get_sec_edgar_mcp_client, get_fred_mcp_client
from examples.utils.logging import (
    setup_logging,
    log_section,
    log_info,
    log_success,
    log_data,
    console,
)

setup_logging()
logger = logging.getLogger(__name__)
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)


def main():
    Config.validate()

    log_section("Investment Research Swarm")
    log_info("Initializing with MCP servers...")

    sec_client = get_sec_edgar_mcp_client()
    fred_client = get_fred_mcp_client()

    log_info("Connecting to SEC EDGAR and FRED MCP servers...")

    with sec_client, fred_client:
        log_success("Successfully connected to MCP servers")

        sec_tools = sec_client.list_tools_sync()
        fred_tools = fred_client.list_tools_sync()

        log_data("SEC EDGAR tools", len(sec_tools))
        log_data("FRED tools", len(fred_tools))

        researcher = Agent(
            name="Data Researcher",
            description="Gathers company and economic data from SEC and FRED",
            system_prompt="""You are a data research specialist with access to SEC EDGAR and FRED.

            Your role:
            - Gather company filings and financial data from SEC
            - Collect relevant economic indicators from FRED
            - Organize data for analysis
            - When data is complete, hand off to Financial Analyst for analysis

            Use handoff_to_analyst() when you've gathered sufficient data.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        analyst = Agent(
            name="Financial Analyst",
            description="Analyzes financial data and company fundamentals",
            system_prompt="""You are a financial analyst specializing in company fundamentals.

            Your role:
            - Analyze company financial statements and metrics
            - Evaluate business performance and trends
            - Identify financial strengths and weaknesses
            - When analysis is complete, hand off to Risk Assessor

            Use handoff_to_risk_assessor() when analysis is ready.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        risk_assessor = Agent(
            name="Risk Assessor",
            description="Evaluates investment risks and concerns",
            system_prompt="""You are a risk assessment specialist.

            Your role:
            - Identify financial, operational, and market risks
            - Evaluate regulatory and competitive risks
            - Assess macroeconomic risk factors
            - When risk analysis is complete, hand off to Strategist

            Use handoff_to_strategist() when risk assessment is done.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        strategist = Agent(
            name="Investment Strategist",
            description="Synthesizes analysis into investment recommendations",
            system_prompt="""You are an investment strategist.

            Your role:
            - Synthesize data, financial analysis, and risk assessment
            - Develop investment thesis and recommendations
            - Provide strategic outlook and action items
            - Create final investment report

            This is the final step - produce comprehensive recommendations.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        swarm = Swarm(
            nodes=[researcher, analyst, risk_assessor, strategist],
            entry_point=researcher,
            max_handoffs=20,
            max_iterations=20,
            execution_timeout=900.0,
            node_timeout=300.0,
            repetitive_handoff_detection_window=8,
            repetitive_handoff_min_unique_agents=3,
        )

        research_request = """Perform comprehensive investment research on Microsoft (MSFT):

        1. Gather latest SEC filings and financial data
        2. Analyze financial health and business performance
        3. Assess key investment risks
        4. Develop investment recommendation with strategic insights

        Collaborate as a team to produce thorough investment analysis."""

        log_section("Swarm Research Request")
        console.print(research_request)

        log_info("Swarm executing research with autonomous collaboration...")

        result = swarm(research_request)

        log_section("Swarm Investment Analysis")
        console.print(result)


if __name__ == "__main__":
    try:
        main()
        log_success("Research completed successfully!")
    except KeyboardInterrupt:
        console.print("\n[warning]Research interrupted by user[/warning]")
    except Exception as e:
        logger.error(f"Research failed: {e}", exc_info=True)
        sys.exit(1)
