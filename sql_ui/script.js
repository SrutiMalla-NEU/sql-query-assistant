// script.js
const API_BASE_URL = "http://127.0.0.1:8000";

function generateSQL() {
  const query = document.getElementById("queryInput").value;
  const sqlOutput = document.getElementById("sqlOutput");
  const sqlQueryText = document.getElementById("sqlQuery");
  const errorMessage = document.getElementById("errorMessage");

  if (!query.trim()) {
    showError("Please enter a query.");
    return;
  }

  hideError();
  sqlQueryText.textContent = "Generating...";
  sqlOutput.classList.remove("d-none");

  axios.post(`${API_BASE_URL}/generate_sql/`, { question: query })
    .then(response => {
      animateTyping(sqlQueryText, response.data.sql_query);
    })
    .catch(() => showError("Error generating SQL. Check your backend/API."));
}

function executeSQL() {
  const sql = document.getElementById("sqlQuery").textContent;
  const queryOutput = document.getElementById("queryOutput");
  const queryResults = document.getElementById("queryResults");

  if (!sql.trim()) {
    showError("No SQL query to execute. Please generate it first.");
    return;
  }

  hideError();
  queryResults.innerHTML = "<em>Executing...</em>";
  queryOutput.classList.remove("d-none");

  axios.post(`${API_BASE_URL}/execute_sql/`, { question: sql })
    .then(response => {
      const results = response.data.execution_result;
      if (Array.isArray(results) && results.length) {
        queryResults.innerHTML = renderTable(results);
      } else {
        queryResults.innerHTML = "<em>No results found.</em>";
      }
    })
    .catch(err => {
      showError("Error executing SQL. Check your backend/API.");
    });
}


function showError(msg) {
  const errorMessage = document.getElementById("errorMessage");
  errorMessage.textContent = msg;
  errorMessage.classList.remove("d-none");
}

function hideError() {
  document.getElementById("errorMessage").classList.add("d-none");
}

function animateTyping(element, text, speed = 15) {
  element.textContent = "";
  let i = 0;
  const interval = setInterval(() => {
    element.textContent += text.charAt(i);
    i++;
    if (i > text.length) clearInterval(interval);
  }, speed);
}

function renderTable(data) {
  if (!Array.isArray(data) || !data.length) return "<em>Empty data</em>";

  const headers = Object.keys(data[0]);
  let html = `<table class="table table-bordered table-dark table-hover table-sm"><thead><tr>`;
  headers.forEach(header => html += `<th>${header}</th>`);
  html += `</tr></thead><tbody>`;
  data.forEach(row => {
    html += `<tr>`;
    headers.forEach(key => {
      let cell = row[key];
      html += `<td>${cell ?? ''}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  return html;
}


window.toggleTheme = function () {
  const html = document.documentElement;
  const current = html.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
};


window.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("theme");
  if (saved) {
    document.documentElement.setAttribute("data-theme", saved);
  }
});

