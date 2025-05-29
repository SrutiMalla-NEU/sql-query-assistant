const API_BASE_URL = "http://127.0.0.1:8000"// Update if deployed

// ✅ Generate SQL from Natural Language Query
function generateSQL() {
    const query = document.getElementById("queryInput").value;
    const sqlOutput = document.getElementById("sqlOutput");
    const sqlQueryText = document.getElementById("sqlQuery");
    const errorMessage = document.getElementById("errorMessage");

    if (!query) {
        errorMessage.textContent = "Please enter a query.";
        errorMessage.classList.remove("d-none");
        return;
    }

    errorMessage.classList.add("d-none");
    sqlOutput.classList.add("d-none");

    axios.post(`${API_BASE_URL}/generate_sql/`, { question: query })
        .then(response => {
            sqlQueryText.textContent = response.data.sql_query;
            sqlOutput.classList.remove("d-none");
        })
        .catch(error => {
            console.error("Error:", error);
            errorMessage.textContent = "Error generating SQL. Check API connection.";
            errorMessage.classList.remove("d-none");
        });
}

// ✅ Execute SQL Query and Show Results
function executeSQL() {
    const query = document.getElementById("queryInput").value;
    const sqlQueryText = document.getElementById("sqlQuery").textContent;
    const resultsContainer = document.getElementById("resultsContainer");
    const resultsHead = document.getElementById("resultsHead");
    const resultsBody = document.getElementById("resultsBody");
    const errorMessage = document.getElementById("errorMessage");

    if (!sqlQueryText) {
        errorMessage.textContent = "Please generate SQL first.";
        errorMessage.classList.remove("d-none");
        return;
    }

    errorMessage.classList.add("d-none");
    resultsContainer.classList.add("d-none");

    axios.post(`${API_BASE_URL}/execute_sql/`, { question: query })
        .then(response => {
            const results = response.data.execution_result;
            if (!results || results.length === 0) {
                errorMessage.textContent = "No results found.";
                errorMessage.classList.remove("d-none");
                return;
            }

            // Clear previous results
            resultsHead.innerHTML = "";
            resultsBody.innerHTML = "";

            // Generate table headers
            const headers = Object.keys(results[0]);
            const headerRow = document.createElement("tr");
            headers.forEach(header => {
                const th = document.createElement("th");
                th.textContent = header;
                th.classList.add("p-2");
                headerRow.appendChild(th);
            });
            resultsHead.appendChild(headerRow);

            // Generate table rows
            results.forEach(row => {
                const tr = document.createElement("tr");
                headers.forEach(header => {
                    const td = document.createElement("td");
                    td.textContent = row[header];
                    td.classList.add("p-2");
                    tr.appendChild(td);
                });
                resultsBody.appendChild(tr);
            });

            resultsContainer.classList.remove("d-none");
        })
        .catch(error => {
            console.error("Error:", error);
            errorMessage.textContent = "Error executing SQL. Check API connection.";
            errorMessage.classList.remove("d-none");
        });
}
