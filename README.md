# SQL Meta Introspection with GPT-4
## Business Problem
Organizations often struggle with accessing and querying complex database schemas efficiently. Data scientists and analysts spend significant time understanding database structures and writing SQL queries. This project implements a natural language-to-SQL solution using GPT-4 and RAG (Retrieval Augmented Generation) to allow users to query the Harvard Growth Lab's Atlas of Economic Complexity "Country Profiles" database using simple English questions.

## Application Description
This application serves as an intelligent SQL query generator that leverages GPT-4 and personal database schema introspection. It enables users to interact with the Harvard Atlas database through natural language queries, which are then converted into accurate SQL statements. The system maintains one database:

harvard_db: Contains the actual country profile data, including products, imports, exports and global market shares.

## RAG Implementation
The RAG approach in this project works by:

Storing database schema information as embeddings.
When a user asks a question using natural language, the RAG retrieves the relevant schema context.
The RAG then combines this context with the user query to help GPT-4 generate accurate SQL, and then uses the generated SQL to query the harvard_db database

Project Structure:
```
|── harvard_trade_data/
    |── data_dictionary.pdf
    |── location_country.csv
    |── product_hs92.csv
    |── services_unilateral_country_product_year_1.dta
    |── services_unilateral_country_product_year_2.dta
    |── services_unilateral_country_product_year_4.dta
    |── services_unilateral_country_product_year_6.dta
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
   git clone https://github.com/mitosisgg/ADS507_FinalProject.git
   cd ADS507_FinalProject/


## Configure
Available variables:

Create a `.env` file from the environment template file `env.example`

Available variables:
| Variable Name          | Description  
|------------------------|-------------------------------------------------|
| OPENAI_API_KEY         | REQUIRED - Your OpenAI API 


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
- PostgreSQL databases (harvard_db)
- Network configurations
- Volume mappings


### database_models.py: Defines SQLAlchemy models for both databases

### harvard_trade_data/ files loaded to DB on app start
- data_dictionary.pdf
- location_country.csv
- product_hs92.csv
- services_unilateral_country_product_year_1.dta
- services_unilateral_country_product_year_2.dta
- services_unilateral_country_product_year_4.dta
- services_unilateral_country_product_year_6.dta



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

## API Usage
Making Requests
Access the API documentation at http://localhost:8000/docs. In the Swagger UI:

1. Navigate to the POST section (green button)
2. Click "Try it out"
3. Input your query in the following format:
```
jsonCopy{
  "question": "how many countries are in the data base",
  "model": "gpt-4",
  "use_rag": true,
  "compare": false
}
```
4. Example Response
The API will return a structured response that can be downloaded:
```
jsonCopy{
  "rag_response": {
    "sql_query": "SELECT COUNT(DISTINCT country_id) FROM country;",
    "database_result": "[(252,)]",
    "explanation": "The result indicates that there are 252 distinct countries in the 'country' database. Each unique country is identified by a unique 'country_id'. The COUNT(DISTINCT country_id) function ensures that each country is only counted once, even if it appears multiple times in the database."
  },
  "non_rag_response": null,
  "comparison": null
}
```
The response includes:

- Generated SQL query (which can be run in the user's RDBMS of choice (SQL Workbench, PostgreSQL, etc)
- Query results from database (the actual answer to the user's natural language question)
- Natural language explanation (what the query is designed to do, or reasons why the question returned a null result)


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
The Harvard Atlas database files are updated on a quarterly basis, aligned with Harvard Growth Lab's data release schedule. This ensures that:

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

## Source Data Reference
The Growth Lab at Harvard University. (2024). International Trade Data (Services) [Data set]. Harvard Dataverse, V1. https://doi.org/10.7910/DVN/NDDMSN
