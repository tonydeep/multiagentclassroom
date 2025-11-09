# SAGE - Multi-Agent Classroom

An interactive learning environment supporting real-time discussions between students and multiple AI agents.

## 🎉 NEW: Claude Agent SDK Implementation

**We now have a simplified demo using Claude Agent SDK!** This new implementation replaces CrewAI with Anthropic's Claude Agent SDK for better performance and easier maintenance.

👉 **[See README_DEMO.md for the new Claude Agent SDK demo](README_DEMO.md)**

### Quick Start (Claude Agent SDK Demo)

```bash
# 1. Install dependencies
pip install -r requirements.txt
npm install -g @anthropic-ai/claude-code

# 2. Set up your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 3. Run the demo
python demo_app.py
```

Then open: **http://localhost:5001**

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
