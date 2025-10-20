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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    Config.validate()

    logger.info("Initializing Market Research Orchestrator with MCP servers...")

    sec_client = get_sec_edgar_mcp_client()
    fred_client = get_fred_mcp_client()

    logger.info("Connecting to SEC EDGAR and FRED MCP servers...")

    with sec_client, fred_client:
        logger.info("Successfully connected to MCP servers")
        logger.info("Retrieving tools from MCP servers...")

        sec_tools = sec_client.list_tools_sync()
        fred_tools = fred_client.list_tools_sync()
        all_tools = sec_tools + fred_tools

        logger.info(f"Retrieved {len(sec_tools)} SEC EDGAR tools")
        logger.info(f"Retrieved {len(fred_tools)} FRED tools")
        logger.info(f"Total tools available: {len(all_tools)}")

        logger.info("\nCreating orchestrator agent...")

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

        logger.info("\n" + "=" * 80)
        logger.info("MARKET RESEARCH REQUEST")
        logger.info("=" * 80)
        logger.info(research_request)
        logger.info("=" * 80 + "\n")

        logger.info("Orchestrator analyzing with SEC and FRED data...\n")

        response = orchestrator(research_request)

        logger.info("\n" + "=" * 80)
        logger.info("MARKET RESEARCH REPORT")
        logger.info("=" * 80)
        logger.info(response)
        logger.info("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nResearch interrupted by user")
    except Exception as e:
        logger.error(f"Research failed: {e}", exc_info=True)
        sys.exit(1)
