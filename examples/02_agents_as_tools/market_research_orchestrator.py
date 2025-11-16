#!/usr/bin/env python3
"""Market Research Orchestrator using Agents as Tools Pattern.

This orchestrator coordinates multiple specialist agents to perform
comprehensive market research combining company filings, economic data, and sector analysis.
All agents use real MCP servers (SEC EDGAR and FRED).
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

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


def main():
    Config.validate()

    log_section("Market Research Orchestrator")
    log_info("Initializing with MCP servers...")

    sec_client = get_sec_edgar_mcp_client()
    fred_client = get_fred_mcp_client()

    log_info("Connecting to SEC EDGAR and FRED MCP servers...")

    with sec_client, fred_client:
        log_success("Successfully connected to MCP servers")
        log_info("Retrieving tools from MCP servers...")

        sec_tools = sec_client.list_tools_sync()
        fred_tools = fred_client.list_tools_sync()
        all_tools = sec_tools + fred_tools

        log_data("SEC EDGAR tools", len(sec_tools))
        log_data("FRED tools", len(fred_tools))
        log_data("Total tools available", len(all_tools))

        log_info("Creating orchestrator agent...")

        orchestrator = Agent(
            name="Market Research Orchestrator",
            description="Coordinates SEC and FRED data for comprehensive market research",
            system_prompt="""You are a senior market research analyst with direct access to:
            - SEC EDGAR: Company filings, financials, and disclosures
            - FRED: Federal Reserve economic data and indicators

            Your methodology:
            1. Gather company data from SEC EDGAR (filings, financials, facts)
            2. Collect relevant economic indicators from FRED
            3. Analyze company within macroeconomic and sector context
            4. Synthesize findings with data-driven insights
            5. Provide actionable investment perspective

            Always provide:
            - Executive summary of key findings
            - Multi-perspective analysis (company + sector + macro)
            - Data-driven insights with specific references
            - Clear investment implications or recommendations""",
            tools=all_tools,
            model=get_default_model(),
        )

        research_request = """Conduct comprehensive market research on Tesla (TSLA):

        1. Company Analysis: Review recent SEC filings for financial health, growth trajectory, and risks
        2. Economic Context: Analyze macroeconomic conditions affecting the EV and automotive sector
        3. Sector Dynamics: Assess Tesla's competitive position in the EV market and broader auto industry

        Provide an integrated analysis with investment perspective."""

        log_section("Market Research Request")
        console.print(research_request)

        log_info("Orchestrator analyzing with SEC and FRED data...")

        response = orchestrator(research_request)

        log_section("Market Research Report")
        console.print(response)


if __name__ == "__main__":
    try:
        main()
        log_success("Research completed successfully!")
    except KeyboardInterrupt:
        console.print("\n[warning]Research interrupted by user[/warning]")
    except Exception as e:
        logger.error(f"Research failed: {e}", exc_info=True)
        sys.exit(1)
