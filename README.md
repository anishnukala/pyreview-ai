AI-Assisted Python Code Review for Beginners
============================================

Overview
--------
This project is a web-based tool that uses Generative AI to provide beginner-friendly feedback on Python code. It analyzes submitted code, highlights errors, suggests readability improvements, and provides improved versions of the code for learning purposes.

Project Poster
--------------
![AI 2010 Project Poster](docs/project-poster.png)

Website Preview
---------------
<details>
<summary>View the full website</summary>

<br>

<img src="docs/website-preview.png" alt="Full AI-assisted Python code review website" width="700">

</details>

Presentation Video
------------------
[Watch the project presentation](docs/project-presentation.m4v)

Prerequisites
-------------
- Python 3.10 or higher
- Google Gemini API key (for Generative AI feedback)
- Internet connection

Setup Instructions
------------------
1. Clone or download the project, then open its root directory.

2. Create and activate a virtual environment.
   Windows:
     venv\Scripts\activate
   Mac/Linux:
     source venv/bin/activate

3. Install the required packages.
     pip install -r requirements.txt

4. Copy `.env.example` to `.env`, then add your Gemini API key.
     GEMINI_API_KEY=your_api_key_here
     GEMINI_MODEL=gemini-2.5-flash
     GEMINI_FALLBACK_MODELS=gemini-2.5-flash-lite

Running the Application
-----------------------
1. Activate your virtual environment (if not already active).
2. Run the Flask app:
     python app.py
3. Open your web browser and go to:
     http://127.0.0.1:5000/
4. Paste a Python code snippet into the text box and click "Analyze Code" to receive AI feedback.

Project Structure
-----------------
```text
AI_FINAL_PROJECT/
├── app.py                # Flask backend
├── data/
│   └── evaluation_table.csv
├── docs/
│   ├── final_applied_ai_project_report.tex
│   ├── project-poster.png
│   ├── project-presentation.m4v
│   └── website-preview.png
├── web_pages/
│   └── index.html        # Frontend HTML
├── .env.example          # Environment variable template
├── .gitignore            # Files excluded from Git
├── requirements.txt      # Python dependencies
└── README.md
```

Notes
-----
- Only supports short Python snippets. Large scripts or multi-file projects are not supported.
- Feedback depends on the AI model; results may vary.
- Requires internet connection and valid API key.
- Keep `.env` private. It is excluded from Git by `.gitignore`.
- The original high-resolution presentation video is retained locally as `docs/project-presentation.mov` and excluded from Git because it exceeds GitHub's regular file-size limit.
- For testing, refer to the "Test Cases" section in the report for examples.

References
----------
- Google Gemini API Documentation: https://ai.google.dev/docs
- OpenAI API Documentation: https://platform.openai.com/docs
- Flask Documentation: https://flask.palletsprojects.com/
- Real Python – Code Quality Best Practices: https://realpython.com
