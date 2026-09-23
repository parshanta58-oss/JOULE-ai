# JOULE-AI: Multi-Agent Enterprise System

**JOULE-AI** is an intelligent enterprise automation system built with LangChain and LangGraph that leverages AI agents to automate business processes across multiple departments including Sales, Finance, HR, Inventory, and Procurement.

## Overview

JOULE-AI is a sophisticated multi-agent system designed to streamline enterprise operations by deploying specialized AI agents for different business functions. Each agent is equipped with domain-specific tools and capabilities to handle complex business queries and automate workflows.

### Key Features

- **Multi-Agent Architecture**: 5 specialized independent agents for different departments
  - **Sales Agent** - Sales analytics, customer management, order tracking
  - **Finance Agent** - Financial analysis and reporting
  - **HR Agent** - Human resources management
  - **Inventory Agent** - Stock and inventory management
  - **Procurement Agent** - Vendor and purchase management

- **Supervisor Agent**: Intelligent routing system that directs queries to appropriate agents
- **Database Integration**: PostgreSQL backend for persistent data storage
- **Real-time Data Access**: Tools for querying and analyzing business data
- **Multi-LLM Support**: Compatible with Groq and Google GenAI models
- **Docker Support**: Easy deployment with Docker Compose

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Supervisor Agent                        │
│            (Routes queries to appropriate agents)           │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───▼────┐         ┌──────▼─────┐        ┌─────▼─────┐
    │  Sales │         │  Finance   │        │     HR    │
    │ Agent  │         │   Agent    │        │   Agent   │
    └────────┘         └────────────┘        └───────────┘
        │                      │                    │
    ┌───▼────-┐         ┌──────▼─────┐              |
    │Inventory│         │Procurement │              |
    │ Agent   │         │   Agent    │              |
    └─────────┘         └────────────┘              |
        |                     |                     |
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                   ┌──────────▼────────┐
                   │   PostgreSQL DB   │
                   │   (joule_ai_db)   │
                   └───────────────────┘
```

## Project Structure

```
JOULE-ai/
├── agents/                          # Agent implementations
│   ├── supervisor.py               # Supervisor/routing agent
│   ├── sales_agent.py              # Sales department agent
│   ├── finance_agent.py            # Finance department agent
│   ├── hr_agent.py                 # HR department agent
│   ├── inventory_agent.py          # Inventory management agent
│   └── procurement_agent.py        # Procurement agent
│
├── tools/                          # Domain-specific tools
│   ├── sales_tools.py              # Sales analytics & queries
│   ├── finance_tools.py            # Financial calculations
│   ├── hr_tools.py                 # HR operations
│   ├── inventory_tools.py          # Inventory management
│   └── procurement_tools.py        # Procurement operations
│
├── database/                       # Database configuration
│   ├── schema.py                   # Database schema definition
│   └── connection.py               # Database connection handler
│
├── data_generation/                # Dummy data generation
│   └── generate_data.py            # Fake data generator
│
├── docker-compose.yml              # PostgreSQL Docker setup
├── requirements.txt                # Python dependencies
└── test_*.py                       # Test files for each component
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional)
- API keys for LLM providers (Groq or Google GenAI)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/parshanta58-oss/JOULE-ai.git
   cd JOULE-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

5. **Start PostgreSQL with Docker**
   ```bash
   docker-compose up -d
   ```

6. **Initialize the database**
   ```bash
   python data_generation/generate_data.py
   ```

## Dependencies

Core dependencies include:

- **LangChain Ecosystem**:
  - `langchain` - Core framework
  - `langchain-core` - Core components
  - `langchain-community` - Community integrations
  - `langgraph` - Graph-based workflow execution

- **LLM Providers**:
  - `langchain-groq` - Groq API integration
  - `langchain-google-genai` - Google Generative AI integration

- **Database**:
  - `psycopg2-binary` - PostgreSQL adapter

- **Utilities**:
  - `Faker` - Dummy data generation
  - `python-dotenv` - Environment variable management

See `requirements.txt` for complete list.

## Usage

### Running Individual Agents

**Sales Agent Example:**
```python
from agents.sales_agent import sales_app
from langchain_core.messages import HumanMessage

query = "What are the total sales for this month?"

response = sales_app.invoke({
    "messages": [HumanMessage(content=query)]
})

print(response["messages"][-1].content)
```

**Finance Agent Example:**
```python
from agents.supervisor import supervisor
from agents.finance_agent import finance_app
from langchain_core.messages import HumanMessage

query = "What is the monthly revenue projection?"

# Use supervisor to route the query
decision = supervisor(query)

if decision == "finance":
    response = finance_app.invoke({
        "messages": [HumanMessage(content=query)]
    })
    print(response["messages"][-1].content)
```

### Using the Supervisor Agent

The Supervisor Agent intelligently routes queries to the appropriate specialized agent:

```python
from agents.supervisor import supervisor
from langchain_core.messages import HumanMessage

query = "Process a new purchase order"
decision = supervisor(query)  # Returns the target agent type
```

## 🗄️ Database Schema

### PostgreSQL Setup

The project uses PostgreSQL running in Docker with the following configuration:

- **Database**: `joule_ai_db`
- **User**: `joule_ai_user`
- **Password**: `joule_ai_password`
- **Port**: 5432

**Key Tables**:
- `customers` - Customer information
- `orders` - Sales orders
- `products` - Product catalog
- `employees` - Employee records
- `inventory` - Stock levels
- `suppliers` - Vendor information
- `financial_records` - Financial transactions

## Testing

Run the included test files to verify agent functionality:

```bash
# Test Sales Agent
python test_sales_agent.py

# Test Sales Tools
python test_sales_tools.py

# Test Finance Agent
python test_finance_agent.py

# Test Finance Tools
python test_finance_tool.py

# Test HR Tools
python test_hr_tool.py

# Test Inventory Tools
python test_inventory_tool.py

# Test Procurement Tools
python test_procurement_tool.py

# Test Supervisor Agent
python test_supervisor_sales.py
```

##  Available Tools

### Sales Tools
- `get_sales_summary()` - Get sales metrics for a date range
- `get_top_customers()` - Identify top performing customers
- `get_customer_sales()` - Get sales for specific customer
- `get_order_details()` - Retrieve order information
- `get_sales_by_product()` - Analyze sales by product

### Finance Tools
- Revenue calculations and projections
- Expense tracking and analysis
- Financial statement generation
- Budget management

### HR Tools
- Employee record management
- Leave tracking
- Payroll processing
- Performance analytics

### Inventory Tools
- Stock level monitoring
- Inventory forecasting
- Stock movement tracking

### Procurement Tools
- Vendor management
- Purchase order tracking
- Supplier performance analysis

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=joule_ai_db
DB_USER=joule_ai_user
DB_PASSWORD=joule_ai_password

# LLM Provider (choose one)
# For Groq
GROQ_API_KEY=your_groq_api_key

# For Google GenAI
GOOGLE_API_KEY=your_google_api_key

# Agent Configuration
MODEL_NAME=llama2-70b-4096  # For Groq
# or
MODEL_NAME=gemini-pro  # For Google GenAI
```

## Development Progress

### ✅ Completed
-  Database schema and setup
-  Dummy data generation with Faker
-  Sales Agent with specialized tools
-  Finance Agent implementation
-  HR, Inventory, and Procurement agents
-  Supervisor agent for intelligent routing
-  Docker Compose configuration
-  Individual component testing

### In Progress
-  Supervisor agent refinement

###  Planned Features
-  Advanced analytics and reporting
-  Real-time notifications
-  Web dashboard interface
-  API REST endpoints
-  Multi-language support
-  Enhanced error handling and logging
-  Performance optimization
-  Unit and integration test suite

##  How It Works

1. **Query Reception**: User submits a query to the system
2. **Supervisor Routing**: Supervisor agent analyzes the query and determines which specialized agent should handle it
3. **Agent Processing**: The selected agent processes the query using its domain-specific tools
4. **Tool Execution**: Tools interact with the PostgreSQL database to retrieve/process data
5. **Response Generation**: The agent formats and returns the response to the user
6. **Output**: Final answer is presented to the user

##  Security Notes

- Use strong database passwords in production
- Store API keys securely (use environment variables)
- Implement authentication/authorization for production deployment
- Validate and sanitize all user inputs
- Use HTTPS for API endpoints

##  Contributing

Contributions are welcome! Please feel free to submit pull requests with improvements or new features.

##  License

This project is open source and available under the MIT License.

##  Author

**Parshanta** - [GitHub Profile](https://github.com/parshanta58-oss)



##  Acknowledgments

- Built with [LangChain](https://www.langchain.com/) and [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [Groq](https://groq.com/) and [Google GenAI](https://ai.google.dev/)
- Data generation with [Faker](https://faker.readthedocs.io/)

---


