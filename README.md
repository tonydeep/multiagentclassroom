# SAGE

A Flask-based interactive learning environment supporting real-time discussions between students and multiple AI agents.

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
