# SAGE - Multi-Agent Classroom

An interactive learning environment supporting real-time discussions between students and multiple AI agents.

## 🚀 **NEW: Professional FastAPI + Next.js Implementation**

**We now have a production-ready implementation using FastAPI and Next.js!** This modern stack offers superior performance, type safety, and developer experience.

### ⚡ Quick Start (Recommended)

```bash
# 1. Clone and setup
git clone <repository-url>
cd multiagentclassroom

# 2. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run with one command
./start.sh
```

Then open: **http://localhost:3000**

👉 **[Full documentation: README_FASTAPI_NEXTJS.md](README_FASTAPI_NEXTJS.md)**

### 🎯 Features

- ✅ **FastAPI** backend with native WebSocket support
- ✅ **Next.js 14** with TypeScript and App Router
- ✅ **Tailwind CSS** for modern, responsive UI
- ✅ **Type-safe** end-to-end (Pydantic + TypeScript)
- ✅ **Auto-generated** API documentation (Swagger UI)
- ✅ **Real-time** agent status updates
- ✅ **Production-ready** architecture

### 📊 Tech Stack Comparison

| Stack | Type Safety | Performance | DX | Production Ready |
|-------|-------------|-------------|----| -----------------|
| **FastAPI + Next.js** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Flask + Socket.IO | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| CrewAI (Original) | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## 📚 Other Implementations

We also have simpler implementations for learning and demonstration:

### Claude Agent SDK Demo (Flask)

Simplified demo using Flask + Socket.IO. Good for learning.

👉 **[See README_DEMO.md](README_DEMO.md)**

```bash
# Quick start
pip install -r requirements.txt
python demo_app.py
# Open: http://localhost:5001
```

---

## Original Implementation (CrewAI)

The original implementation using CrewAI is still available below:

# Demo (May take some time to load)
![Demo](demo.gif)

## Setup and Installation

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd multiagentclassroom
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or .\venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   Create a `.env` file with:
   ```
   GOOGLE_API_KEY=your_google_api_key
   FLASK_SECRET_KEY=your_secret_key
   # GEMINI_API_KEY= # in case GOOGLE_API_KEY doesn't work
   ```
   ### Note: Use paid API with high rate limits to operate the system properly. Free API keys won't work due to RPM limitations.
5. **Run application**
   ```bash
   flask run
   ```

Access the application at `http://127.0.0.1:5000`

## Usage Notes

- **Default Script**: Use the default script to run scenarios as described in the paper
- **Creative Scenario Generation**: Optional feature to create new scenarios with keywords
- **Script Planner Module**: Currently not integrated into the main system. Can be used separately with:
  ```bash
  python -u flow/scriptPlannerFlow.py
  ```
  Modify inputs in `flow/scriptPlannerFlow.py` as needed
- **Dialog Module**: Only basic dynamic script generation is integrated, loop functionality not yet implemented
