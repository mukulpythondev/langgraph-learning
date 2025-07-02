# LangGraph Learning Project

This repository demonstrates a basic LangGraph setup with streaming, modular graphs, and human-in-the-loop support.

---

## 📁 Project Structure

```bash
.
├── main.py              # Simple static LangGraph flow
└── app/
    ├── main.py         # Streaming LangGraph execution
    ├── graph.py        # Nodes, edges, and graph logic
    └── support.py      # Human-in-the-loop tool
```

---

## ⚙️ Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/mukulpythondev/langgraph-learning.git
cd langgraph-learning
pip install -r requirements.txt
```

---

### 2. Add Environment Variables

Create a `.env` file at the project root:

```env
OPENAI_API_KEY=sk-proj-...
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="lsv2_pt_..."
LANGSMITH_PROJECT="langgraph-test"
```

> **Note**: Keep this file private and do not commit it.

---

### 3. Start MongoDB (Checkpointer)

Spin up MongoDB locally using Docker:

```bash
docker run -d -p 27017:27017 --name mongo-checkpoint mongo
```

---

## 🚀 Running the Graphs

### Static Flow

```bash
python main.py
```

### Streaming Graph with Human Loop

```bash
python app/main.py
```

---

## 🧩 Purpose

Built for hands-on learning of LangGraph:

* Node/edge architecture
* Streamable execution
* Human-assisted steps

