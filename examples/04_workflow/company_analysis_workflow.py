#!/usr/bin/env python3
"""Company Analysis Graph/Workflow Example.

This example demonstrates the Graph pattern for structured, dependency-based
task orchestration with parallel execution using GraphBuilder.
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from strands import Agent
from strands.multiagent import GraphBuilder

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

    log_section("Company Analysis Workflow")
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

        # Create specialized agents for workflow nodes
        data_gatherer = Agent(
            name="Data Gatherer",
            description="Gathers company filings and economic data",
            system_prompt="""You are a data gathering specialist with access to SEC EDGAR and FRED.

            Your role:
            - Gather recent SEC filings (10-K, 10-Q, 8-K) for the target company
            - Collect relevant economic indicators from FRED
            - Organize data for downstream analysis
            - Focus on gathering comprehensive data, not analysis

            Output structured data ready for financial and risk analysis.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        financial_analyst = Agent(
            name="Financial Analyst",
            description="Analyzes financial statements and metrics",
            system_prompt="""You are a financial analysis specialist.

            Your role:
            - Analyze company financial statements from SEC filings
            - Calculate key financial ratios and metrics
            - Evaluate financial health and trends
            - Identify strengths and weaknesses

            Provide quantitative financial assessment with specific metrics.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        risk_analyst = Agent(
            name="Risk Analyst",
            description="Evaluates investment and business risks",
            system_prompt="""You are a risk analysis specialist.

            Your role:
            - Identify financial, operational, and market risks
            - Evaluate regulatory and competitive risks
            - Assess macroeconomic risk factors
            - Quantify risk severity and likelihood

            Provide comprehensive risk assessment with mitigation considerations.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        report_synthesizer = Agent(
            name="Report Synthesizer",
            description="Synthesizes analysis into final investment report",
            system_prompt="""You are an investment report specialist.

            Your role:
            - Synthesize findings from data gathering, financial analysis, and risk analysis
            - Create comprehensive investment thesis
            - Provide clear recommendations
            - Present actionable insights

            Create a professional investment report with executive summary and detailed analysis.""",
            tools=sec_tools + fred_tools,
            model=get_default_model(),
        )

        # Build the workflow graph
        log_info("Building analysis workflow graph...")

        builder = GraphBuilder()

        # Add nodes
        builder.add_node(data_gatherer, "data_gathering")
        builder.add_node(financial_analyst, "financial_analysis")
        builder.add_node(risk_analyst, "risk_analysis")
        builder.add_node(report_synthesizer, "synthesis")

        # Define dependencies (DAG structure)
        # Data gathering is the entry point
        builder.add_edge("data_gathering", "financial_analysis")
        builder.add_edge("data_gathering", "risk_analysis")

        # Both analyses feed into synthesis
        builder.add_edge("financial_analysis", "synthesis")
        builder.add_edge("risk_analysis", "synthesis")

        # Set entry point
        builder.set_entry_point("data_gathering")

        # Configure execution parameters
        builder.set_execution_timeout(900.0)  # 15 minutes
        builder.set_node_timeout(300.0)  # 5 minutes per node

        # Build the graph
        graph = builder.build()

        log_success("Graph built successfully!")
        log_info("Graph structure:")
        console.print(
            "  [cyan]data_gathering[/cyan] → [[cyan]financial_analysis[/cyan], [cyan]risk_analysis[/cyan]]"
        )
        console.print(
            "  [[cyan]financial_analysis[/cyan], [cyan]risk_analysis[/cyan]] → [cyan]synthesis[/cyan]"
        )
        log_info("Note: financial_analysis and risk_analysis will execute in parallel")

        ticker = "AAPL"
        analysis_request = f"""Perform comprehensive investment analysis on {ticker}:

        1. Gather latest SEC filings and relevant economic data
        2. Conduct financial analysis of business performance and health
        3. Perform risk analysis of investment and business risks
        4. Synthesize findings into investment recommendation

        Execute the workflow to completion."""

        log_section("Workflow Request")
        log_data("Ticker", ticker)
        console.print(analysis_request)

        log_info("Executing graph workflow...")

        result = graph(analysis_request)

        log_section("Workflow Execution Summary")
        log_data("Status", result.status)
        log_data("Total nodes", result.total_nodes)
        log_data("Completed", result.completed_nodes)
        log_data("Failed", result.failed_nodes)
        log_data("Execution time", f"{result.execution_time}ms")
        log_data("Execution order", [node.node_id for node in result.execution_order])

        log_section("Investment Analysis Report")

        # Get final synthesized report
        synthesis_result = result.results["synthesis"].result
        console.print(synthesis_result)


if __name__ == "__main__":
    try:
        main()
        log_success("Analysis completed successfully!")
    except KeyboardInterrupt:
        console.print("\n[warning]Analysis interrupted by user[/warning]")
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        sys.exit(1)
