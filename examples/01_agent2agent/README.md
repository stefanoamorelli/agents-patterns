# Agent2Agent (A2A) Pattern Example

## Overview

This example demonstrates the Agent-to-Agent (A2A) protocol pattern, which enables seamless communication between AI agents across different platforms and implementations.

## Pattern Characteristics

- **Cross-platform communication** - Agents can discover and communicate with each other using a standardized protocol
- **Distributed architecture** - Agents run as independent servers that can be deployed separately
- **Service discovery** - Clients can discover agent capabilities through agent cards
- **Protocol-based interaction** - Uses standardized A2A message format for agent-to-agent communication

## Use Case: Financial Analysis with Distributed Agents

This example shows how to:

1. **Deploy SEC EDGAR agent as an A2A server** - Exposes SEC filing analysis capabilities
2. **Deploy FRED agent as an A2A server** - Exposes economic data analysis capabilities
3. **Create orchestrator agent** - Discovers and coordinates multiple A2A agents
4. **Perform comprehensive analysis** - Combines insights from multiple specialized agents

## Files

- `sec_edgar_server.py` - A2A server exposing SEC EDGAR analysis
- `fred_server.py` - A2A server exposing FRED economic data analysis
- `financial_analyst_a2a.py` - Orchestrator that coordinates multiple A2A agents
- `a2a_client_example.py` - Direct A2A client communication example

## Running the Example

### Step 1: Start the A2A Servers

Terminal 1 - SEC EDGAR Agent:
```bash
python examples/01_agent2agent/sec_edgar_server.py
```

Terminal 2 - FRED Agent:
```bash
python examples/01_agent2agent/fred_server.py
```

### Step 2: Run the Orchestrator

Terminal 3 - Financial Analyst:
```bash
python examples/01_agent2agent/financial_analyst_a2a.py
```

## Key Concepts

### A2A Server
- Wraps a Strands Agent and exposes it via A2A protocol
- Runs on HTTP and responds to A2A message requests
- Publishes agent card describing capabilities

### A2A Client
- Discovers agents via agent card resolution
- Sends standardized A2A messages
- Can operate in sync or streaming mode

### A2A as Tool
- Agents can wrap other A2A agents as tools
- Enables dynamic agent discovery and composition
- Maintains standard tool interface for orchestration

## Benefits

- **Scalability** - Deploy specialized agents independently
- **Reusability** - Same agent can serve multiple clients
- **Interoperability** - Works across different agent frameworks
- **Flexibility** - Easy to add/remove specialized agents

## When to Use

- Distributed multi-agent systems
- Agent marketplaces
- Cross-platform agent integration
- Microservices-style agent architectures
- When agents need to be deployed and scaled independently
