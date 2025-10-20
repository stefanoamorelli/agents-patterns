# Workflow Pattern Example

## Overview

This example demonstrates the Workflow pattern, where tasks are orchestrated in a structured way with explicit dependencies and parallel execution where possible.

## Pattern Characteristics

- **Structured execution** - Pre-defined task graph with clear dependencies
- **Deterministic flow** - Execution order determined by task dependencies
- **Parallel execution** - Independent tasks run concurrently
- **Dependency management** - Tasks wait for their dependencies to complete
- **State tracking** - Detailed progress monitoring and task status

## Use Case: Comprehensive Company Analysis Pipeline

This example shows how to:

1. **Define workflow tasks** - Create tasks with dependencies
2. **Configure agents per task** - Assign specialized agents to tasks
3. **Execute workflow** - Run tasks in correct order with parallelization
4. **Monitor progress** - Track task completion and overall status

## Files

- `company_analysis_workflow.py` - Main workflow implementation
- `workflow_tasks.py` - Task definitions and configurations

## Running the Example

```bash
python examples/04_workflow/company_analysis_workflow.py
```

## Key Concepts

### Task Definition
Each task specifies:
- **task_id** - Unique identifier
- **description** - What the task should accomplish
- **system_prompt** - Specialized instructions for the task
- **dependencies** - Tasks that must complete first
- **priority** - Execution priority when multiple tasks are ready

### Dependency Graph
```
data_extraction (P:5)
    ├→ financial_analysis (P:4)
    │   └→ valuation_model (P:2)
    └→ competitive_analysis (P:4)
        └→ valuation_model (P:2)
            └→ final_report (P:1)

economic_analysis (P:5, parallel with data_extraction)
    └→ valuation_model (P:2)

P = Priority (higher runs first when ready)
```

### Workflow Execution
The workflow tool:
- Resolves dependencies automatically
- Runs independent tasks in parallel
- Passes task outputs to dependent tasks
- Manages retries and error handling
- Tracks overall progress

## Example Workflow Structure

```python
tasks = [
    {
        "task_id": "data_extraction",
        "description": "Extract financial data from SEC filings",
        "system_prompt": "You extract structured financial data...",
        "dependencies": [],
        "priority": 5
    },
    {
        "task_id": "financial_analysis",
        "description": "Analyze financial metrics and trends",
        "system_prompt": "You analyze financial performance...",
        "dependencies": ["data_extraction"],
        "priority": 4
    },
    # ... more tasks
]
```

## Benefits

- **Reliability** - Deterministic execution with clear error handling
- **Efficiency** - Parallel execution maximizes throughput
- **Clarity** - Explicit dependencies make workflow easy to understand
- **Repeatability** - Same workflow produces consistent results
- **Monitoring** - Detailed progress and status tracking

## When to Use

- Multi-step processes with clear dependencies
- Repeatable, structured workflows
- When parallel execution improves efficiency
- Long-running processes requiring monitoring
- Tasks requiring specific execution order
- Workflows that need pause/resume capabilities

## Advanced Features

### Pause and Resume
```python
# Pause workflow
agent.tool.workflow(action="pause", workflow_id="analysis")

# Resume later
agent.tool.workflow(action="resume", workflow_id="analysis")
```

### Status Monitoring
```python
status = agent.tool.workflow(action="status", workflow_id="analysis")
# Returns: progress percentage, task statuses, execution times
```

### Resource Management
- Dynamic thread allocation
- Rate limiting with exponential backoff
- Task prioritization
- Automatic retry on failure
