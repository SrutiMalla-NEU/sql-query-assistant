from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import CORS Middleware
from pydantic import BaseModel
import mysql.connector
import google.generativeai as genai
from sqlalchemy import create_engine, MetaData
from urllib.parse import quote_plus  

# ✅ Configure Google Gemini AI
genai.configure(api_key="AIzaSyDJDrQ1WS1wi-Uy8IdQOx80Owigz2fN3Uo")   # Replace with your actual API key

# ✅ MySQL Database Credentials
MYSQL_USER = "root"
MYSQL_PASSWORD = "Srutimalla08@"  
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "sql_query_assistant"

# ✅ Encode password for special characters
ENCODED_PASSWORD = quote_plus(MYSQL_PASSWORD)

# ✅ SQLAlchemy Connection String
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{ENCODED_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

# ✅ Create MySQL database connection
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
metadata = MetaData()

app = FastAPI()

# ✅ Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # ✅ Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # ✅ Allow all headers
)


# ✅ Request Model for Query Execution
class QueryRequest(BaseModel):
    question: str  # User's natural language input

# 🔹 Function to Retrieve Schema Dynamically
def get_schema_info():
    """
    Retrieves the schema information from the database dynamically.
    """
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        cursor = connection.cursor()

        # Query to fetch table column details
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE();
        """)

        schema_info = {}
        for table_name, column_name, data_type in cursor.fetchall():
            if table_name not in schema_info:
                schema_info[table_name] = []
            schema_info[table_name].append(f"{column_name} ({data_type})")

        cursor.close()
        connection.close()

        return schema_info  # Returns a dictionary with table names and columns
    except Exception as e:
        return {"error": f"Error retrieving schema: {e}"}

# 🔹 Function to Convert Natural Language to SQL Using Gemini AI
def natural_language_to_sql(user_input):
    """
    Uses Google Gemini AI to convert a natural language query into an SQL query.
    Dynamically retrieves schema info for better accuracy.
    """
    schema_info = get_schema_info()  # Fetch schema dynamically

    if "error" in schema_info:
        return schema_info  # Return error if schema retrieval fails

    schema_text = "\n".join([f"Table: {table}\nColumns: {', '.join(columns)}" for table, columns in schema_info.items()])

    prompt = f"""
    Convert the following natural language request into a MySQL query:
    Request: {user_input}
    
    Use the following database schema information:
    {schema_text}

    Instructions:
    - Generate an SQL query based on the given schema.
    - Ensure all column and table names match exactly.
    - If the request is unclear, make a logical assumption based on the schema.
    - DO NOT include markdown formatting (```sql ... ```). Return only the SQL query.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  
        response = model.generate_content(prompt)  

        # Extract SQL from AI response
        if hasattr(response, 'text'):
            sql_query = response.text.strip()
        elif hasattr(response, 'candidates'):
            sql_query = response.candidates[0].content.strip()
        else:
            return {"error": "Unexpected AI response format"}

        # ✅ Remove Markdown Formatting (` ```sql ... ``` `)
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        return {"sql_query": sql_query}  # ✅ Return clean SQL query
    except Exception as e:
        return {"error": f"Error generating SQL: {e}"}

# 🔹 Function to Execute SQL Queries
def execute_query(query):
    """
    Executes SQL queries and handles SELECT, INSERT, UPDATE, DELETE.
    """
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        cursor = connection.cursor(dictionary=True)

        query_type = query.strip().split()[0].upper()  # Detect query type

        cursor.execute(query)

        if query_type == "SELECT":
            result = cursor.fetchall()  # ✅ Fetch data for SELECT queries
        else:
            connection.commit()  # ✅ Commit changes for INSERT, UPDATE, DELETE
            result = {"message": f"✅ Query executed successfully! ({query_type})"}

        cursor.close()
        connection.close()
        return {"sql_query": query, "execution_result": result}  # ✅ Return both query and result

    except mysql.connector.Error as e:
        return {"error": f"❌ Error executing query: {e}"}


# 🔹 FastAPI Endpoint: Convert NL to SQL
@app.post("/generate_sql/")
def generate_sql(request: QueryRequest):
    """
    API Endpoint: Convert a natural language question into an SQL query.
    """
    return natural_language_to_sql(request.question)

# 🔹 FastAPI Endpoint: Execute SQL Query
@app.post("/execute_sql/")
def execute_sql(request: QueryRequest):
    """
    API Endpoint: Convert NL to SQL and execute the query.
    """
    sql_response = natural_language_to_sql(request.question)
    
    if "error" in sql_response:
        return sql_response  # Return error if SQL generation fails

    sql_query = sql_response["sql_query"]
    execution_result = execute_query(sql_query)

    return {"sql_query": sql_query, "execution_result": execution_result}

# 🔹 FastAPI Endpoint: Get Schema Info
@app.get("/get_schema/")
def get_schema():
    """
    API Endpoint: Retrieve schema information dynamically.
    """
    return get_schema_info()
