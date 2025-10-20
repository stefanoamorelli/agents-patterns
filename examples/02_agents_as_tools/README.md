# Agents as Tools Pattern Example

## Overview

This example demonstrates the Agents as Tools pattern, where specialized agents are wrapped as tools that can be invoked by an orchestrator agent.

## Pattern Characteristics

- **Single orchestrator** - One agent coordinates all specialist agents
- **Agents as tools** - Specialist agents are exposed through the tool interface
- **Clear separation of concerns** - Each specialist has a specific domain
- **Synchronous coordination** - Orchestrator decides when to invoke which specialist
- **Reusable specialists** - Same specialist can be used in different contexts

## Use Case: Market Research Platform

This example shows how to:

1. **Create specialist agents** - SEC analyst, Economic analyst, Sector analyst
2. **Wrap agents as tools** - Using @tool decorator or tool functions
3. **Build orchestrator** - Main agent that coordinates specialists
4. **Execute research workflow** - Multi-perspective company and market analysis

## Files

- `market_research_orchestrator.py` - Main orchestrator coordinating specialist agents
- `specialists.py` - Specialist agent definitions (SEC, FRED, Sector analysts)

## Running the Example

```bash
python examples/02_agents_as_tools/market_research_orchestrator.py
```

## Key Concepts

### Specialist Agents
Each specialist agent:
- Has specific domain expertise
- Has dedicated tools for its domain
- Can be invoked as a tool by the orchestrator
- Returns structured insights

### Orchestrator Agent
The orchestrator:
- Has access to all specialist agents as tools
- Decides which specialists to consult
- Synthesizes findings from multiple specialists
- Provides comprehensive analysis

### Benefits Over Direct Tool Access
- **Encapsulation** - Complex tool chains hidden within specialists
- **Expertise modeling** - Each specialist has domain-specific prompts
- **Reusability** - Specialists can be used in multiple orchestrators
- **Maintainability** - Changes to specialist logic don't affect orchestrator

## Example Workflow

```
User Request: "Analyze Tesla's investment potential"
    ↓
Orchestrator Agent
    ├→ SEC Analyst Tool
    │  └→ Returns: Financial metrics, recent filings
    ├→ Economic Analyst Tool
    │  └→ Returns: Macro trends, EV market indicators
    └→ Sector Analyst Tool
       └→ Returns: Competitive analysis, industry trends
    ↓
Orchestrator synthesizes all findings
    ↓
Comprehensive investment analysis
```

## When to Use

- Single-process agent coordination
- Clear delegation of specialized tasks
- When orchestrator needs full control over execution order
- Reusable specialist agents across different use cases
- When specialist agent details should be hidden from orchestrator
