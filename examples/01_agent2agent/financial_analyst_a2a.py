#!/usr/bin/env python3
"""Financial Analyst using A2A Protocol.

This orchestrator coordinates multiple A2A agents to perform comprehensive
financial analysis combining SEC filings and economic data.
"""
import asyncio
import logging
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, TextPart

from strands import Agent, tool

from examples.utils.config import Config
from examples.utils.models import get_default_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 300


def create_message(*, role: Role = Role.user, text: str) -> Message:
    return Message(
        kind="message",
        role=role,
        parts=[Part(TextPart(kind="text", text=text))],
        message_id=uuid4().hex,
    )


class A2AAgentTool:
    """Wrapper to call A2A agents as tools."""

    def __init__(self, agent_url: str, agent_name: str):
        self.agent_url = agent_url
        self.agent_name = agent_name
        self.agent_card = None

    async def _ensure_initialized(self):
        """Discover agent card if not already done."""
        if self.agent_card is None:
            async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as httpx_client:
                resolver = A2ACardResolver(httpx_client=httpx_client, base_url=self.agent_url)
                self.agent_card = await resolver.get_agent_card()
                logger.info(f"Discovered {self.agent_name} at {self.agent_url}")

    async def call_agent(self, message: str) -> str:
        """Send a message to the A2A agent and return response."""
        await self._ensure_initialized()

        try:
            async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as httpx_client:
                config = ClientConfig(httpx_client=httpx_client, streaming=False)
                factory = ClientFactory(config)
                client = factory.create(self.agent_card)

                msg = create_message(text=message)

                async for event in client.send_message(msg):
                    if isinstance(event, Message):
                        response_text = ""
                        for part in event.parts:
                            if hasattr(part, 'text'):
                                response_text += part.text
                        return response_text

                return f"No response received from {self.agent_name}"

        except Exception as e:
            logger.error(f"Error calling {self.agent_name}: {e}")
            return f"Error contacting {self.agent_name}: {str(e)}"


async def main():
    Config.validate()

    logger.info("Initializing Financial Analyst A2A Orchestrator...")

    # Create A2A agent tools
    sec_agent = A2AAgentTool("http://127.0.0.1:9000", "SEC EDGAR Analyst")
    fred_agent = A2AAgentTool("http://127.0.0.1:9001", "FRED Economic Analyst")

    # Wrap as Strands tools
    @tool
    async def call_sec_edgar_analyst(query: str) -> str:
        """
        Call the SEC EDGAR analyst agent to analyze company filings and financial data.

        Args:
            query: Question or analysis request about SEC filings, company financials, or disclosures

        Returns:
            Analysis from SEC EDGAR specialist
        """
        return await sec_agent.call_agent(query)

    @tool
    async def call_fred_analyst(query: str) -> str:
        """
        Call the FRED economic analyst agent to analyze macroeconomic data and trends.

        Args:
            query: Question or analysis request about economic indicators, GDP, unemployment, etc.

        Returns:
            Analysis from FRED economic specialist
        """
        return await fred_agent.call_agent(query)

    # Create orchestrator with A2A tools
    orchestrator = Agent(
        name="Financial Analyst Orchestrator",
        description="Coordinates SEC EDGAR and FRED specialist agents via A2A protocol",
        system_prompt="""You are a senior financial analyst orchestrating specialized A2A agents.

        Available agents:
        1. call_sec_edgar_analyst - Expert in SEC filings, company financials, and disclosures
        2. call_fred_analyst - Expert in macroeconomic data, trends, and FRED indicators

        Your approach:
        1. Delegate SEC filing questions to the SEC EDGAR analyst
        2. Delegate economic data questions to the FRED analyst
        3. Synthesize insights from both agents
        4. Provide comprehensive analysis combining company-specific and macroeconomic perspectives

        Always coordinate agent findings into coherent, actionable insights.""",
        tools=[call_sec_edgar_analyst, call_fred_analyst],
        model=get_default_model(),
    )

    analysis_request = """Perform comprehensive analysis of Apple Inc (AAPL):

    1. Get the latest 10-K filing and extract key financial metrics
    2. Analyze recent economic indicators (GDP, unemployment, tech sector trends)
    3. Assess how current macroeconomic conditions may impact Apple's business
    4. Provide investment perspective considering both company fundamentals and economic context
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
