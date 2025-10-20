#!/usr/bin/env python3
"""SEC EDGAR A2A Server.

This server exposes a SEC EDGAR analyst agent via the A2A protocol,
using the real SEC EDGAR MCP server for data access.
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from strands import Agent
from strands.multiagent.a2a import A2AServer

from examples.utils.config import Config
from examples.utils.models import get_default_model
from examples.utils.mcp_tools import get_sec_edgar_mcp_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    Config.validate()

    logger.info("Starting SEC EDGAR A2A Server...")

    sec_client = get_sec_edgar_mcp_client()

    logger.info("Connecting to SEC EDGAR MCP server...")

    with sec_client:
        logger.info("Successfully connected to SEC EDGAR MCP server")

        sec_tools = sec_client.list_tools_sync()
        logger.info(f"Retrieved {len(sec_tools)} SEC EDGAR tools")

        agent = Agent(
            name="SEC EDGAR Analyst",
            description="Expert analyst for SEC filings and corporate disclosures. Analyzes 10-K, 10-Q, 8-K filings and company financials.",
            system_prompt="""You are an expert SEC filing analyst with access to the SEC EDGAR database.

            Your capabilities:
            - Retrieve and analyze company filings (10-K, 10-Q, 8-K, etc.)
            - Extract financial data from SEC submissions
            - Analyze company facts and metrics
            - Provide insights on business performance and risks

            Always cite specific filing dates and document references in your analysis.""",
            tools=sec_tools,
            model=get_default_model(),
        )

        logger.info("Creating A2A server on port 9000...")

        server = A2AServer(
            agent=agent,
            host="127.0.0.1",
            port=9000
        )

        logger.info("=" * 80)
        logger.info("SEC EDGAR A2A Server running on http://127.0.0.1:9000")
        logger.info("Agent Card: http://127.0.0.1:9000/.well-known/ai-agent.json")
        logger.info("=" * 80)

        server.serve()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
    except Exception as e:
        logger.error(f"Server failed: {e}", exc_info=True)
        sys.exit(1)
