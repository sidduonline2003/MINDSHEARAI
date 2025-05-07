# AI-Powered Smart Learning Assistant

An intelligent learning platform that combines multiple AI tools to enhance the learning experience.

## Features

### 1. Smart Notes Generator
- Generates structured study notes with visuals
- Uses Google Gemini for text generation
- Integrates image scraping and validation
- Exports to editable PDF format

### 2. PDF Query Engine
- Answers questions from uploaded PDFs
- Uses LangChain and FAISS for efficient document processing
- Provides accurate, context-aware responses

### 3. Research AI Tool
- Fetches academic research summaries
- Provides citations and source links
- Integrates with DeepSeek R1 API

### 4. Humanize AI Tool
- Converts AI-generated text into natural language
- Supports multiple tone options
- Enhances readability and engagement

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/CSS/JavaScript
- **AI Models**: Google Gemini, CLIP
- **Vector Database**: FAISS
- **PDF Processing**: PyPDF2, pdfkit
- **Research API**: DeepSeek R1

## Setup

1. Clone the repository
```bash
git clone [repository-url]
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the application
```bash
uvicorn app.main:app --reload
```

## Environment Variables

Create a `.env` file with the following variables:
```
GOOGLE_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
SERPAPI_API_KEY=your_serpapi_key
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 