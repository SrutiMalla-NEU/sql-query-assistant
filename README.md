# 🧠 SQL Query Assistant

An AI-powered full-stack web app that converts natural language questions into SQL queries and executes them live on a connected MySQL database.

## Features

- Natural Language to SQL conversion using Google Gemini API
- Real-time query execution on MySQL
- Frontend with Bootstrap, HTML, CSS, and JavaScript
- FastAPI backend for clean API design
- CORS enabled, clean separation of frontend/backend

## Tech Stack

- **Frontend**: HTML, CSS, Bootstrap, JavaScript (Axios)
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **AI Integration**: Google Gemini (Generative AI)
- **ORM**: SQLAlchemy

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/sql-query-assistant.git
cd sql-query-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start MySQL Server

Make sure your MySQL DB is running and matches the config in `app.py`:
```python
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_DATABASE = "sql_query_assistant"
```

### 4. Run FastAPI Server

```bash
uvicorn app:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to interact with the API.

### 5. Launch Frontend

Open `sql_ui/index.html` directly in your browser.

## 💡 Example Prompt

```
Show me all employees from the HR department
```

Returns:
```sql
SELECT * FROM employees WHERE department = 'HR';
```

## Screenshots



## Future Enhancements

- ✅ Save query history
- ✅ Add user authentication
- ✅ Dark mode support
- ✅ Export results to CSV
- ✅ Host on Render / Vercel / Railway

## 🤝 Contributing

Feel free to fork this repo, raise issues or open PRs!

Built by Sruti Smitha Malla(https://www.linkedin.com/in/yourprofile)
