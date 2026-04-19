# 🧠 Conversational Data Explorer (Agentic AI System)

A lightweight AI-powered application that allows users to upload spreadsheets and interact with their data using natural language. The system leverages an **agentic architecture (LangGraph)** to interpret queries, generate insights, and create visualizations automatically.

---

## 🚀 Features

- 📂 Upload CSV / Excel files  
- 💬 Ask questions in natural language  
- 🔁 Supports follow-up queries (context-aware)  
- 📊 Automatic data visualization (charts)  
- 🔍 Drill-down analysis  
- 🧠 Intelligent query understanding using LLM agents  
- ⚡ Hybrid caching (exact + semantic)

---

## ⚙️ Project Setup


---

## 🧩 Backend Setup (FastAPI)

### 1️⃣ Navigate to backend

```bash
cd backend
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

#### Activate:
##### Windows:

```bash
venv\Scripts\activate
```

##### Mac/Linux:

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Remove .txt from .env.txt and place you Gemini API Key.

### 5️⃣ Run FastAPI server

```bash
uvicorn main:app --reload
```
Server will run at:

```bash
http://localhost:8000
```

## 🌐 Frontend Setup (React)


### 1️⃣ Navigate frontend

```bash
cd frontend
```

### 2️⃣ Install dependencies

```bash
npm install
```

### 3️⃣ Start frontend

```bash
npm run dev
```

App will run at:
```bash
http://localhost:5173
```

## 🏗️ System Architecture

### 🔹 High-Level Flow:
1. User uploads dataset
2. Ingestion agent generates dataset context
3. User asks query
4. LangGraph orchestrates multiple agents
5. Response + optional visualization returned to UI

### 🔹 System Design:


### 🔹 Agentic Workflow (LangGraph):


## 🤖 Agents Overview

### 1️⃣ Ingestion Agent

#### Goal:
Understand uploaded dataset and generate structured context which will be used by further agents to be awar about the dataset uploaded.

#### Input:

1. Column names
2. Sample rows
3. Data types

#### Output:

1. Dataset description
2. Column explanations

### 2️⃣ Input Guardrail Agent

#### Goal:
1. Validate user query
2. Handle greetings
3. Detect out-of-scope queries
4. Answer from conversation history if possible
5. Contextualize query

#### Input:

1. User query
2. Dataset context
3. Conversation history

#### Output:

A JSON of this format:
{
  "isContinue": <true or false>,
  "contextualized_user_query": <enhanced user query based on the conversation history+dataset context>,
  "query": <if further processing isn't required then provides a conversational response which will be shown to the user.>
}

### 3️⃣ Pandas Query Generator Agent

#### Goal:
Convert natural language into executable pandas expression

#### Input:

1. Contextualized user query
2. Dataset context

#### Output:

A pandas expression with 'df' as variable name. Example:
df.groupby("column")["value"].sum()

### 4️⃣ Query Validator Agent

#### Goal:
1. Validate generated pandas query
2. Improve it for better context

#### Input:

1. Generated pandas expression
2. Dataset context
3. User query

#### Output:

Improved or same pandas expression as the generator agent

### 5️⃣ Pandas Query Executor (Non LLM)

#### Goal:
Execute generated query safely

#### Input:

1. Pandas DataFrame with df variable
2. Validated Pandas expression

#### Output:

A JSON type of output:
{
  "type": "dataframe / series / scalar",
  "data": ...
}

### 6️⃣ Visualization Agent

#### Goal:
Decide if visualization is needed as per the data and which type

#### Supported Types:

1. bar
2. horizontal_bar
3. line
4. pie
5. scatter


#### Input:

1. User query
2. Query result
3. Dataset context

#### Output:

A JSON type of output:
{
  "recommended_visualization": "bar",
  "reason": "..."
}

### 7️⃣ Data Formatter (Non LLM)

#### Goal:
Convert query result into plottable format

#### Input:

1. Chart Type
2. Query result

#### Output:

A formatted JSON as per the type of chat suggested

### 8️⃣ Chart Generator (Non LLM)

#### Goal:
Generate visualization using matplotlib and return base64 image

#### Input:

1. Formatted Data
2. Chart Type

#### Output:

Base64 encoded visualization

### 9️⃣ Natural Language Response Agent

#### Goal:
Convert structured result into human-readable answer

#### Input:

1. Query Result
2. Contextualized User Query

#### Output:

A final natural language response of the fetched data.

## 🧠 Conversation Handling

1. Maintains:
    1. Last 4 messages as it is(window).
    2. Older messages are summarized
2. Enables:
    1. Follow-up queries
    2. Context retention

## ⚡ Caching Layer (Integration pending)

Hybrid caching implemented:
1. Exact Match Cache:
    1. Hash-based lookup
2. Semantic Cache:
    1. Uses embeddings
    2. Cosine similarity matching

## 🛠️ Tech Stack

### Backend
1. FastAPI
2. LangGraph
3. Pandas
4. Matplotlib
5. Gemini API

### Frontend (v minimal)
1. React JS
2. Axios

## 📌 Future Improvements
1. Query Validation refinement
2. Advanced visualization (multi-axis, dashboards)
3. Persistent storage (DB)
4. Streaming responses
5. Better UI
6. Multi-file support


#### Feel free to connect w me on linkedIn: https://linkedin.com/in/arif9353