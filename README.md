# AI Resume Analyzer

A beginner-friendly AI portfolio project built with Python and Streamlit.  
The app analyzes a resume, checks ATS-style keywords, identifies missing skills from a job description, and gives improvement suggestions.

## Why this project matters

This project is useful for entry-level AI, data analyst, AI business analyst, and AI operations roles because it shows practical skills in:

- Python
- Streamlit app development
- Resume text extraction
- Keyword analysis
- ATS-style scoring
- Optional OpenAI API integration
- Business-focused AI use cases

## Features

- Upload a resume as PDF or TXT
- Paste a job description
- Get an ATS-style score
- Detect AI, data, business, and analytics keywords
- Identify missing skills from the job description
- Check for important resume sections
- Get improvement recommendations
- Optional deeper AI feedback using OpenAI API

## Project structure

```text
ai-resume-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── sample_resumes/
│   └── sample_resume.txt
└── .streamlit/
    └── config.toml
```

## How to run locally

### 1. Clone the repo

```bash
git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Mac/Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

## Optional: Use OpenAI API

The app works without an API key using rule-based scoring.

For deeper AI feedback, create a `.env` file or environment variable:

```bash
OPENAI_API_KEY=your_api_key_here
```

Never upload your real API key to GitHub.

## Example use cases

- AI Business Analyst resume review
- Data Analyst resume review
- Junior AI Engineer resume improvement
- Business Intelligence resume optimization
- Internship resume keyword matching

## Future improvements

- Add DOCX support
- Export analysis as PDF
- Add charts for skills match
- Add login system
- Add multiple resume comparison
- Deploy on Streamlit Community Cloud

## Author

Built as an AI portfolio project.
