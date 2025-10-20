# Swarm Pattern Example

## Overview

This example demonstrates the Swarm pattern, where multiple specialized agents collaborate autonomously with shared context to solve complex tasks through dynamic handoffs.

## Pattern Characteristics

- **Self-organizing** - Agents decide when to hand off to each other
- **Shared context** - All agents access full task history and knowledge
- **Autonomous coordination** - No central controller, agents coordinate via handoffs
- **Dynamic task distribution** - Work flows based on agent expertise
- **Emergent intelligence** - Collective problem-solving through collaboration

## Use Case: Investment Research Team

This example shows how to:

1. **Create specialist agents** - Researcher, Analyst, Risk Assessor, Strategist
2. **Configure swarm** - Set handoff limits, timeouts, and safety mechanisms
3. **Execute collaborative research** - Agents autonomously hand off to each other
4. **Track swarm execution** - Monitor agent handoffs and collaboration

## Files

- `investment_research_swarm.py` - Main swarm implementation
- `swarm_agents.py` - Specialist agent definitions for the swarm

## Running the Example

```bash
python examples/03_swarm/investment_research_swarm.py
```

## Key Concepts

### Swarm Agents
Each agent in the swarm:
- Has specific expertise and tools
- Can see the full collaboration history
- Decides when to hand off to another agent
- Contributes knowledge to shared context

### Handoff Tool
Agents use `handoff_to_agent` to transfer control:
```python
handoff_to_agent(
    agent_name="analyst",
    message="I've gathered the data, need quantitative analysis",
    context={"data_sources": ["10-K", "FRED GDP"]}
)
```

### Shared Context
All agents see:
- Original user request
- History of agent handoffs
- Knowledge contributed by previous agents
- List of available agents for collaboration

### Safety Mechanisms
- **max_handoffs** - Limits total handoffs (default: 20)
- **execution_timeout** - Total swarm timeout (default: 15 min)
- **node_timeout** - Individual agent timeout (default: 5 min)
- **repetitive_handoff_detection** - Prevents ping-pong between agents

## Example Workflow

```
User: "Analyze Amazon for investment potential"
    ↓
Researcher Agent (entry point)
    ├→ Gathers SEC filings and economic data
    └→ Handoff to Analyst Agent
         ├→ Performs quantitative analysis
         └→ Handoff to Risk Assessor Agent
              ├→ Evaluates investment risks
              └→ Handoff to Strategist Agent
                   └→ Synthesizes findings → Final Report
```

## Benefits

- **Flexible collaboration** - Agents determine optimal workflow
- **Comprehensive analysis** - Multiple perspectives emerge naturally
- **Efficient specialization** - Each agent focuses on its expertise
- **Emergent problem-solving** - Solution approach emerges from collaboration

## When to Use

- Complex problems requiring multiple perspectives
- Tasks benefiting from specialist collaboration
- When execution path should emerge dynamically
- Exploratory or creative problem-solving
- When different viewpoints enhance quality

## Advanced Configuration

```python
swarm = Swarm(
    agents=[researcher, analyst, risk_assessor, strategist],
    entry_point=researcher,
    max_handoffs=20,
    max_iterations=20,
    execution_timeout=900.0,  # 15 minutes
    node_timeout=300.0,       # 5 minutes per agent
    repetitive_handoff_detection_window=8,
    repetitive_handoff_min_unique_agents=3
)
```
