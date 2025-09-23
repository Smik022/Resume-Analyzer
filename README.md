# Resume Analyzer

An AI-powered application that analyzes resumes and provides detailed feedback using Google's Gemini AI.

## Features

- Upload PDF and DOCX resume files
- Extract text content from resumes
- AI-powered analysis of resume content
- Scoring based on ATS compatibility 
- Section-by-section improvement suggestions
- Modern React frontend with progress indicators
- RESTful Django backend API

## Tech Stack

### Backend
- Django
- Django REST Framework
- Google Generative AI (Gemini)
- PDF Plumber (PDF parsing)
- python-docx (DOCX parsing)

### Frontend
- React
- CSS3 with modern animations 
- Fetch API for backend communication

## Setup

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Resume-Analyzer.git
cd Resume-Analyzer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the Django development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

## API Endpoints

### Upload Resume
- **URL**: `/api/analyzer/upload/`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameter**: file (PDF/DOCX)
- **Response**: 
```json
{
    "id": "resume_id",
    "file": "file_url",
    "text": "extracted_text",
    "uploaded_at": "timestamp"
}
```

### Analyze Resume
- **URL**: `/api/analyzer/analyze/`
- **Method**: POST
- **Content-Type**: application/json
- **Body**: 
```json
{
    "resume_id": "id"
}
```
- **Response**:
```json
{
    "overall_score": 85,
    "ats_score": 90,
    "improvement_suggestions": {
        "skills": ["suggestion1", "suggestion2"],
        "experience": ["suggestion1", "suggestion2"],
        "education": ["suggestion1", "suggestion2"],
        "summary": ["suggestion1", "suggestion2"]
    }
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.
