#!/usr/bin/env python3
"""Financial Analyst using A2A Protocol.

This orchestrator uses the Strands A2A Client Tool to discover and interact
with A2A agents for comprehensive financial analysis.
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from strands import Agent
from strands_tools.a2a_client import A2AClientToolProvider

from examples.utils.config import Config
from examples.utils.models import get_default_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    Config.validate()

    logger.info("Initializing Financial Analyst A2A Orchestrator...")

    # Create A2A client tool provider with known agent URLs
    # These agents should be running on the specified ports
    a2a_provider = A2AClientToolProvider(
        known_agent_urls=[
            "http://127.0.0.1:9000",  # SEC EDGAR Analyst
            "http://127.0.0.1:9001",  # FRED Economic Analyst
        ]
    )

    logger.info("A2A Client Tool Provider initialized with known agents")

    # Create orchestrator with A2A client tools
    # The provider automatically discovers agents and creates appropriate tools
    orchestrator = Agent(
        name="Financial Analyst Orchestrator",
        description="Coordinates SEC EDGAR and FRED specialist agents via A2A protocol",
        system_prompt="""You are a senior financial analyst orchestrating specialized A2A agents.

        You have access to A2A client tools that can discover and interact with available agents.

        Your approach:
        1. Discover available A2A agents using the provided tools
        2. Delegate SEC filing questions to the SEC EDGAR analyst
        3. Delegate economic data questions to the FRED analyst
        4. Synthesize insights from both agents
        5. Provide comprehensive analysis combining company-specific and macroeconomic perspectives

        Always coordinate agent findings into coherent, actionable insights.""",
        tools=a2a_provider.tools,
        model=get_default_model(),
    )

    analysis_request = """Perform comprehensive analysis of Apple Inc (AAPL):

    1. Get the latest 10-K filing and extract key financial metrics (revenue, net income, cash flow)
    2. Analyze recent economic indicators:
       - Latest GDP growth rate
       - Current unemployment rate
       - Recent inflation trends (limit to last 2 years)
    3. Assess how current macroeconomic conditions may impact Apple's business
    4. Provide investment perspective considering both company fundamentals and economic context

    IMPORTANT: Keep queries focused and limit data retrieval to recent periods only.
    """

    logger.info("\n" + "=" * 80)
    logger.info("A2A ORCHESTRATOR REQUEST")
    logger.info("=" * 80)
    logger.info(analysis_request)
    logger.info("=" * 80 + "\n")

    logger.info("Orchestrator coordinating A2A agents...\n")

    response = await orchestrator.invoke_async(analysis_request)

    logger.info("\n" + "=" * 80)
    logger.info("COMPREHENSIVE ANALYSIS")
    logger.info("=" * 80)
    logger.info(response)
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nAnalysis interrupted by user")
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        sys.exit(1)
