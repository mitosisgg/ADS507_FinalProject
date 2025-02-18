# SQL Meta Introspection with GPT-4
## Business Problem
Organizations often struggle with accessing and querying complex database schemas efficiently. Data scientists and analysts spend significant time understanding database structures and writing SQL queries. This project implements a natural language to SQL solution using GPT-4 and RAG (Retrieval Augmented Generation) to allow users to query the Harvard Atlas Country Profiles database using simple English questions.

## Application Description
This application serves as an intelligent SQL query generator that leverages GPT-4 and database schema introspection. It enables users to interact with the Harvard Atlas database through natural language queries, which are then converted into accurate SQL statements. The system maintains two databases:

harvard_db: Contains the actual country profile data
schema_db: Stores metadata about harvard_db's structure for context enhancement

## RAG Implementation
The RAG approach in this project works by:

Storing database schema information as embeddings
When a user asks a question, retrieving relevant schema context
Combining this context with the user query to help GPT-4 generate accurate SQL
Using the generated SQL to query the harvard_db database

Project Structure:
```
|── SQL/
    |── country.py
    |── product.py
    |── services1.py
    |── services2.py
    |── services4.py
    |── services6.py
|── .gitattributes
|── .gitignore
|── env.example
|── docker-compose.yml
|── Dockerfile
|── app.py
|── CONTRIBUTING.md
|── database_models.py
|── env.example
|── LICENSE
|── README.md
|── requirements.txt
|── utils.py
```

## Requirements

Before building the Docker image, make sure you have the following installed on your local machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo


## Configure
Available variables:

Create a `.env` file from the environment template file `env.example`

Available variables:
| Variable Name          | Description  
|------------------------|-------------------------------------------------|
| OPENAI_API_KEY         | REQUIRED - Your OpenAI API key for GPT-4                                 
| DB_USER                | REQUIRED - PostgreSQL database username                                
| DB_PASSWORD            | REQUIRED - PostgreSQL database password                               
| DB_NAME                | REQUIRED - PostgreSQL database name (harvard_db)                           
| DB_HOST                | REQUIRED - PostgreSQL database host address


## Docker Implementation
### Why Docker?
Docker provides several key advantages for this project:

Consistent development environment across team members
Easy deployment and scaling
Isolation of dependencies and services
Simple management of multiple services (API, databases)

## Key Docker Files

### Dockerfile: Defines the application environment, including:

- Python 3.10 base image
- Required system dependencies
- Application code and dependencies
- Runtime configurations


### docker-compose.yml: Orchestrates services:

- Application service
- PostgreSQL databases (harvard_db and schema_db)
- Network configurations
Volume mappings


### database_models.py: Defines SQLAlchemy models for both databases

### SQL folder
 - country.py
 - product.py
 - services1.py
 - service2.py
 - services4.py
 - services6.py
  Data will be loaded from local files:
    ```
    - Replace '/Users/katherinekimberling/ADS507_FinalProject/' for your local path
    - Add .csv files


### app.py: Main application logic including:

- API endpoints
- Database connections
- GPT-4 integration
- Query processing


### utils.py: Helper functions for:

- Database operations
- Schema introspection
- Query generation


## Building and Running

Setup Environment:

- Clone repository and navigate to project directory
```bash
    git clone <repository-url>
    cd <project-directory>
```
###  Rename Git and Docker configuration files
```
mv Docker/ditattributes .gitattributes
```
```
mv Docker/dockerignore .dockerignore
```
```
mv Docker/ditignore .gitignore
```

### Create .env file from template
```
cp env.example .env
```

### Edit .env with your configurations

## Build and Start Services:

**To start everything**
```
docker compose up
```
If changes to build scripts have been made, **rebuild**.
```
docker compose up --build
```

To enter **watch mode** (auto rebuild on file changes).
First start everything, then in new terminal:
```
docker compose watch
```

**Shutdown**
If health check fails or containers don't start up as expected, shutdown
completely to start up again.
```
docker compose down
```

## Access the Application:

- UI Check: http://localhost:8000/
- API Documentation: http://localhost:8000/docs

## Security Considerations

## Environment Variables:

Never commit `.env` files to version control
Rotate API keys regularly
Use minimal required permissions
Store sensitive data in secure credential stores


## Access Control:

Implement API authentication
Use HTTPS in production
Regular security audits
Proper database user permissions


## Maintenance
Data Updates:
The Harvard Atlas database files are updated on a quarterly basis, aligned with Harvard's data release schedule. This ensures that:

- Country profile data remains current with Harvard's latest publications
- Historical data consistency is maintained
- Data quality aligns with Harvard's standards

## Version Control
Docker image versions are managed with a strict update policy:

- New versions are released after comprehensive testing
- Security audits must be completed before version updates
- Each release includes detailed changelog documentation
- Version numbers follow semantic versioning (MAJOR.MINOR.PATCH)

## License
Included in the LICENSE file