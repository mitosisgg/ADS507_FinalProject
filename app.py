from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database_models import get_db, init_db, seed_database, DATABASE_URL
from sqlalchemy import func, text, create_engine, inspect
import asyncio
import openai
import os
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="GenAI Comparison API")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("LLM", "gpt-4")

class QueryRequest(BaseModel):
    question: str = 'What is the total export value converted in billions of services in France Italy and United States of America in 1992 individualy?'
    model: Optional[str] = DEFAULT_MODEL
    use_rag: bool = True
    compare: bool = False

class RAGResponse(BaseModel):
    sql_query: Optional[str]
    database_result: Optional[str]
    explanation: str

class ComparisonResponse(BaseModel):
    rag_response: RAGResponse
    non_rag_response: Optional[RAGResponse]
    comparison: Optional[str]

# Database introspection code
def introspect_database():
    # Create a database connection
    engine = create_engine(DATABASE_URL)
    
    # Create an inspector object
    inspector = inspect(engine)
    
    # Get table names
    table_names = inspector.get_table_names()
    
    # Initialize a dictionary to store schema information
    schema_info = {}
    
    # Iterate over table names and retrieve column information
    for table_name in table_names:
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({'name': column['name'], 'type': str(column['type'])})
        schema_info[table_name] = columns
    
    return schema_info

# Call the database introspection function during application startup
@app.on_event("startup")
async def startup_event():
    init_db()
    global database_schema
    database_schema = introspect_database()
    print("Database schema:")
    print(database_schema)
    asyncio.create_task(seed_database())

@app.get("/")
async def root():
    return {"status": "healthy", "message": "GenAI API is running"}

@app.post("/query", response_model=ComparisonResponse)
async def query(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        model = request.model or DEFAULT_MODEL
        
        if request.use_rag:
            # Generate SQL query using GPT
            prompt = f"""
            Given this question: "{request.question}"
            Generate a SQL query for our academic database that includes:
            {str(database_schema)}

            Return only the SQL query, nothing else.
            """

            sql_response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            
            sql_query = sql_response.choices[0].message.content.strip()
            
            # Execute the query
            result = db.execute(text(sql_query)).fetchall()
            result_str = str(result)

            # Generate explanation with context
            rag_explanation = openai.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": f"The question was: '{request.question}'\nSQL query: {sql_query}\nResults: {result_str}\nExplain these results."
                }],
                temperature=0.7
            ).choices[0].message.content

            rag_response = RAGResponse(
                sql_query=sql_query,
                database_result=result_str,
                explanation=rag_explanation
            )
        else:
            rag_response = RAGResponse(
                sql_query=None,
                database_result=None,
                explanation="RAG response not requested"
            )

        # Get non-RAG response if comparison requested
        non_rag_response = None
        if request.compare:
            non_rag_prompt = f"Please answer this question about an academic database: {request.question}"
            non_rag_completion = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": non_rag_prompt}],
                temperature=0.7
            )
            non_rag_response = RAGResponse(
                sql_query=None,
                database_result=None,
                explanation=non_rag_completion.choices[0].message.content
            )

        # Generate comparison if both responses exist
        comparison = None
        if request.compare and rag_response and non_rag_response:
            comparison_completion = openai.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": f"Compare these responses:\n\nRAG: {rag_response.explanation}\n\nNon-RAG: {non_rag_response.explanation}"
                }],
                temperature=0.7
            )
            comparison = comparison_completion.choices[0].message.content

        return ComparisonResponse(
            rag_response=rag_response,
            non_rag_response=non_rag_response,
            comparison=comparison
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)