"""Specialist Agents for Investment Research Swarm.

This module defines the specialist agents that collaborate in the swarm.
Each agent has specific expertise and contributes to collective intelligence.
"""
from strands import Agent

from examples.utils.mcp_tools import (
    fred_get_series,
    fred_search,
    sec_get_company_facts,
    sec_get_company_filings,
)
from examples.utils.models import get_default_model


def create_researcher_agent() -> Agent:
    return Agent(
        name="researcher",
        description="Gathers comprehensive data from SEC filings and economic sources",
        system_prompt="""You are a meticulous financial researcher.

        Your role in the swarm:
        - Gather SEC filings (10-K, 10-Q, 8-K) for target companies
        - Retrieve relevant economic indicators from FRED
        - Collect industry and sector data
        - Identify data sources for analysis

        When you've gathered sufficient data, hand off to the 'analyst' for quantitative analysis.
        Share data sources and key findings in the handoff context.

        Focus on breadth and coverage of relevant information sources.""",
        tools=[sec_get_company_filings, sec_get_company_facts, fred_search, fred_get_series],
        model=get_default_model(),
    )


def create_analyst_agent() -> Agent:
    return Agent(
        name="analyst",
        description="Performs quantitative analysis and identifies financial trends",
        system_prompt="""You are a quantitative financial analyst.

        Your role in the swarm:
        - Analyze financial metrics and ratios
        - Identify trends in revenue, profitability, cash flow
        - Compare against industry benchmarks
        - Evaluate growth trajectories and margins
        - Assess financial health and sustainability

        When you've completed quantitative analysis, hand off to 'risk_assessor'
        to evaluate risks and potential downsides.
        Share key metrics and trends in the handoff context.

        Focus on data-driven insights and numerical precision.""",
        tools=[sec_get_company_facts, fred_get_series],
        model=get_default_model(),
    )


def create_risk_assessor_agent() -> Agent:
    return Agent(
        name="risk_assessor",
        description="Evaluates investment risks and potential downsides",
        system_prompt="""You are a risk assessment specialist.

        Your role in the swarm:
        - Identify business risks (competition, regulation, technology)
        - Evaluate financial risks (leverage, liquidity, volatility)
        - Assess macroeconomic risks (rates, recession, sector headwinds)
        - Consider operational and strategic risks
        - Estimate downside scenarios

        When you've completed risk assessment, hand off to 'strategist'
        for final synthesis and recommendations.
        Share identified risks and severity in the handoff context.

        Focus on comprehensive risk identification and prudent evaluation.""",
        tools=[sec_get_company_filings, fred_search, fred_get_series],
        model=get_default_model(),
    )


def create_strategist_agent() -> Agent:
    return Agent(
        name="strategist",
        description="Synthesizes all findings into strategic recommendations",
        system_prompt="""You are a senior investment strategist.

        Your role in the swarm:
        - Synthesize findings from researcher, analyst, and risk assessor
        - Develop investment thesis (bull/bear cases)
        - Provide clear recommendation (buy/hold/sell) with rationale
        - Identify key catalysts and monitoring points
        - Articulate risk-reward profile

        You are typically the final agent in the swarm.
        Produce a comprehensive investment recommendation that incorporates
        all previous findings.

        Focus on strategic clarity and actionable recommendations.""",
        tools=[],
        model=get_default_model(),
    )
