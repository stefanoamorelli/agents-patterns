#!/usr/bin/env python3
"""FRED Economic Data A2A Server.

This server exposes a FRED economic analyst agent via the A2A protocol,
using the real FRED MCP server for data access.
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from strands import Agent
from strands.multiagent.a2a import A2AServer

from examples.utils.config import Config
from examples.utils.models import get_default_model
from examples.utils.mcp_tools import get_fred_mcp_client
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

    log_section("FRED Economic Data A2A Server")
    log_info("Starting server...")

    fred_client = get_fred_mcp_client()

    log_info("Connecting to FRED MCP server...")

    with fred_client:
        log_success("Successfully connected to FRED MCP server")

        fred_tools = fred_client.list_tools_sync()
        log_data("Retrieved FRED tools", len(fred_tools))

        agent = Agent(
            name="FRED Economic Analyst",
            description="Expert economist specializing in Federal Reserve Economic Data. Analyzes 800,000+ economic time series including GDP, unemployment, inflation, and interest rates.",
            system_prompt="""You are an expert macroeconomic analyst with access to comprehensive FRED data.

            Your capabilities:
            - Search and retrieve economic time series data
            - Analyze macroeconomic trends and indicators
            - Compare historical data and identify patterns
            - Provide economic context for business decisions

            CRITICAL: To avoid overwhelming the context:
            - When searching, use specific keywords and limit results to top 5-10 series
            - When browsing, focus on specific categories rather than broad exploration
            - When retrieving series data, limit date ranges to recent periods (last 1-5 years)
            - Prioritize the most relevant indicators for the query
            - Never attempt to retrieve or analyze hundreds of series at once

            Always cite specific series IDs and date ranges in your analysis.""",
            tools=fred_tools,
            model=get_default_model(),
        )

        log_info("Creating A2A server on port 9001...")

        server = A2AServer(agent=agent, host="127.0.0.1", port=9001)

        log_section("Server Ready")
        log_success("FRED A2A Server running on http://127.0.0.1:9001")
        log_data("Agent Card", "http://127.0.0.1:9001/.well-known/agent-card.json")

        server.serve()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[warning]Server stopped by user[/warning]")
    except Exception as e:
        logger.error(f"Server failed: {e}", exc_info=True)
        sys.exit(1)
