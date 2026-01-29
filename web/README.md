# FlowCast Web Application

Modern React + Tailwind frontend with FastAPI backend.

## Quick Start

### Windows
```bash
# Double-click start_dev.bat or run:
cd web
start_dev.bat
```

### Manual Start

**Terminal 1 - Backend:**
```bash
cd web/backend
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd web/frontend
npm install
npm run dev
```

## Access

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Tech Stack

### Frontend
- React 18
- Vite (build tool)
- Tailwind CSS
- TypeScript
- Lucide React (icons)

### Backend
- FastAPI
- Python 3.x
- Reuses existing FlowCast modules (parser, metrics, forecaster, insights, charts)

## Features

- Drag & drop file upload
- Real-time analysis
- Beautiful dark theme (inspired by Linear/Notion)
- Equal-height card layouts
- Smooth animations
- Export to Excel/ZIP
