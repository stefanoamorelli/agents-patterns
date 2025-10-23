# Agents Patterns

> [!IMPORTANT]
> This is a demo repository created for the presentation at AWS Dev Day Copenhagen 2025. It is intended for educational purposes and experimentation. **Not meant for production use.**

This repository demonstrates four different multi-agents patterns (A2A, Agents as Tools, Swarm, DAGs) using [Claude](https://www.anthropic.com/claude), the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), and the [Strands SDK](https://github.com/joshuavial/strands).

**Resources:**
- [Presentation Slides](https://docs.google.com/presentation/d/10mm5Bqztkj15zadAWk_jcvjjEjoZJ0Id3oAU2arCF-0/edit?usp=sharing)
- [AWS Dev Day Copenhagen Event](https://aws-experience.com/emea/north/xe/69ffe/aws-dev-day-copenhagen-reimagining-the-developer-experience)

## Prerequisites

- Python 3.10+
- Node.js 18+ (for FRED MCP server)
- Anthropic API key
- FRED API key (free - [sign up and request a key](https://fred.stlouisfed.org/docs/api/api_key.html))

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/stefanoamorelli/agents-patterns.git
cd agents-patterns
```

### 2. Set Up MCP Servers

Clone and install the required MCP servers as sibling directories:

```bash
cd ..

# Clone and install SEC EDGAR MCP server
git clone https://github.com/stefanoamorelli/sec-edgar-mcp
cd sec-edgar-mcp
pip install .  # Install dependencies inside sec-edgar-mcp directory
cd ..

# Clone and install FRED MCP server
git clone https://github.com/stefanoamorelli/fred-mcp-server
cd fred-mcp-server
npm install  # Install dependencies inside fred-mcp-server directory
npm run build  # Build the TypeScript server
cd ..

# Return to agents-patterns directory
cd agents-patterns
```

Your directory structure should look like:
```
parent-directory/
├── agents-patterns/
├── sec-edgar-mcp/
└── fred-mcp-server/
```

### 3. Install Dependencies

```bash
pip install .
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit the `.env` file with your actual credentials:
- `ANTHROPIC_API_KEY`: Your Anthropic API key (this project uses Claude by default)
- `FRED_API_KEY`: Your FRED API key from [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)
- `SEC_EDGAR_USER_AGENT`: Your name and email in the format "Your Name your.email@example.com"

Export the environment variables:
```bash
export $(cat .env | xargs)
```

Or use a tool like `python-dotenv` to load them automatically.

## Agent Patterns

This repository demonstrates four agentic patterns:

### 1. Agent-to-Agent (A2A)
Agents collaborate by delegating specialized tasks to each other.
```bash
python examples/01_agent2agent/financial_analyst_a2a.py
```

### 2. Agents as Tools
Agents are encapsulated as tools that can be invoked by an orchestrator.
```bash
python examples/02_agents_as_tools/market_research_orchestrator.py
```

### 3. Swarm Pattern
Agents dynamically hand off control to specialized agents based on context.
```bash
python examples/03_swarm/investment_research_swarm.py
```

### 4. Workflow Pattern
Agents follow a structured workflow with defined stages and dependencies.
```bash
python examples/04_workflow/company_analysis_workflow.py
```

## Testing the Agents

Each pattern can be tested independently. Here are example commands:

```bash
# Test Agent-to-Agent pattern
cd examples/01_agent2agent
python financial_analyst_a2a.py

# Test Agents as Tools pattern
cd examples/02_agents_as_tools
python market_research_orchestrator.py

# Test Swarm pattern
cd examples/03_swarm
python investment_research_swarm.py

# Test Workflow pattern
cd examples/04_workflow
python company_analysis_workflow.py
```

## Troubleshooting

### MCP Server Not Found
If you get an error about MCP servers not being found:
- Ensure the MCP servers are cloned in sibling directories
- Or set the environment variables `SEC_EDGAR_MCP_PATH` and `FRED_MCP_PATH` to the correct paths

### API Key Errors
Ensure all required environment variables are set:
- `ANTHROPIC_API_KEY` for Claude API access
- `FRED_API_KEY` for economic data
- `SEC_EDGAR_USER_AGENT` for SEC EDGAR API access
