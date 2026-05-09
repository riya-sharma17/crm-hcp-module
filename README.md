
# CRM HCP Module — AI-First Interaction Logger

An AI-powered CRM system for pharmaceutical field representatives to log 
interactions with Healthcare Professionals (HCPs).

## 🚀 Live Demo
- Frontend: http://65.2.10.232:5173
- Backend API: http://65.2.10.232:8000
- API Docs: http://65.2.10.232:8000/docs

## 🛠 Tech Stack
| Layer | Technology |
|---|---|
| Frontend | React + Vite + Redux |
| Backend | Python + FastAPI |
| AI Agent | LangGraph |
| LLM | Groq (llama-3.3-70b-versatile) |
| Database | PostgreSQL |
| Deployment | AWS EC2 + Docker |

## ✨ Key Features
- **Dual Interface**: Log interactions via structured form OR AI chat
- **Auto Form Fill**: AI extracts data from chat and fills form automatically
- **LangGraph Agent**: 5 tools for sales activities
- **Docker**: One command to run everything

## 🤖 LangGraph Tools
1. **log_interaction** — Captures and saves HCP interaction data
2. **edit_interaction** — Modifies existing logged interactions
3. **search_hcp** — Searches HCPs by name/specialty/city
4. **suggest_followups** — AI-powered next step suggestions
5. **get_interaction_history** — Retrieves past HCP interactions

## 🏃 Run Locally

### Prerequisites
- Docker Desktop
- Git

### Steps
```bash
git clone https://github.com/riya-sharma17/crm-hcp-module.git
cd crm-hcp-module
echo "GROQ_API_KEY=your_key_here" > .env
docker-compose up --build
```

Open http://localhost:5173

### Without Docker
**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure
```
crm-hcp-module/
├── frontend/          # React + Redux
│   ├── src/
│   │   ├── components/
│   │   │   ├── form/  # Left panel
│   │   │   └── chat/  # Right panel
│   │   ├── store/     # Redux slices
│   │   └── services/  # API calls
├── backend/           # FastAPI
│   └── app/
│       ├── agent/     # LangGraph
│       ├── api/       # Routes
│       ├── models/    # DB tables
│       └── schemas/   # Validation
└── docker-compose.yml
```

## 🎥 Video Walkthrough
[[Link to video]](https://drive.google.com/file/d/1zLU5d23YfY21Uy6HGJi1XZFIvEZV284o/view?usp=drivesdk)
```


