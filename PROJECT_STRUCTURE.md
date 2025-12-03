# Project Structure

```
.
├── backend/                          # Python Flask Backend
│   ├── app.py                        # Main Flask application with API endpoints
│   ├── requirements.txt              # Python dependencies
│   ├── generate_sample_data.py       # Sample data generator for testing
│   ├── uploads/                      # Uploaded CSV files (auto-created)
│   └── .gitignore                    # Backend-specific gitignore
│
├── frontend/                         # React Frontend
│   ├── public/
│   │   └── index.html                # HTML template
│   ├── src/
│   │   ├── App.js                    # Main React component
│   │   ├── index.js                  # React entry point
│   │   ├── index.css                 # Global styles
│   │   └── components/
│   │       ├── FileUpload.js         # CSV upload component
│   │       ├── ReportViewer.js       # Report display component
│   │       └── ChatBot.js            # Chatbot Q&A component
│   ├── package.json                  # Node.js dependencies
│   └── .gitignore                    # Frontend-specific gitignore
│
├── start.bat                         # Windows script to start both servers
├── start_backend.bat                 # Windows script for backend only
├── start_frontend.bat                # Windows script for frontend only
│
├── README.md                         # Main project documentation
├── QUICKSTART.md                     # Quick start guide
├── SAMPLE_DATA.md                    # Sample data format guide
├── PROJECT_STRUCTURE.md              # This file
└── .gitignore                        # Root gitignore

```

## Key Files Explained

### Backend (`backend/app.py`)

Main Flask application with the following endpoints:

- **`POST /api/upload`**: Upload CSV file and generate analytics report
- **`POST /api/chat`**: Chat with AI assistant about the report
- **`POST /api/export/pdf`**: Export report as PDF
- **`GET /api/health`**: Health check endpoint

Key functions:
- `analyze_dataframe()`: Extracts summary statistics from CSV
- `generate_report_with_gemini()`: Uses Gemini AI to generate comprehensive report

### Frontend Components

#### `App.js`
Main application component with tab navigation:
- Upload tab
- Report tab
- Chat tab

#### `FileUpload.js`
Drag-and-drop CSV file upload component using react-dropzone

#### `ReportViewer.js`
Displays the generated report with:
- Executive summary
- KPIs in card format
- Expandable sections for detailed analysis
- PDF export functionality

#### `ChatBot.js`
Interactive chatbot for Q&A about the report using the `/api/chat` endpoint

## Data Flow

1. **Upload**: User uploads CSV → Backend parses → Analyzes structure
2. **Analysis**: Backend sends data summary to Gemini AI → Receives comprehensive report
3. **Display**: Frontend receives JSON report → Renders in organized sections
4. **Chat**: User asks question → Backend sends context + question to Gemini → Returns answer
5. **Export**: User clicks export → Backend generates PDF → Downloads to user

## API Response Structure

The `/api/upload` endpoint returns:

```json
{
  "data_understanding": "...",
  "kpis": [...],
  "trend_analysis": "...",
  "anomaly_detection": "...",
  "correlation_analysis": "...",
  "insights": [...],
  "executive_summary": "...",
  "business_recommendations": [...],
  "slide_deck": {
    "slide_1_title": "...",
    "slide_2_kpis": [...],
    "slide_3_charts": "...",
    "slide_4_insights": [...],
    "slide_5_anomalies": [...],
    "slide_6_recommendations": [...],
    "slide_7_summary": "..."
  },
  "chatbot_format": {
    "kpis": [...],
    "insights": [...],
    "summary": "...",
    "recommendations": [...],
    "anomalies": [...],
    "chart_explanations": [...],
    "trend_analysis": "...",
    "columns": [...],
    "chatbot_memory": {...}
  },
  "metadata": {
    "filename": "...",
    "upload_date": "...",
    "total_rows": 123,
    "total_columns": 10
  }
}
```

## Technology Stack

### Backend
- **Flask**: Web framework
- **Pandas**: Data processing
- **Google Generative AI**: Gemini API for AI analysis
- **ReportLab**: PDF generation
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React 18**: UI framework
- **Material-UI**: Component library
- **Axios**: HTTP client
- **React-Dropzone**: File upload

## Configuration

### Gemini API Key
Currently configured in `backend/app.py` line 28. For production, consider using environment variables.

### Ports
- Backend: `5000` (configurable in `app.py`)
- Frontend: `3000` (default React port)

### File Limits
- Maximum file size: 16MB (configurable in `app.py`)
- Supported format: CSV only

## Development Workflow

1. Start backend: `cd backend && python app.py`
2. Start frontend: `cd frontend && npm start`
3. Open browser: `http://localhost:3000`
4. Upload CSV and view report
5. Test chatbot functionality
6. Export PDF if needed

## Future Enhancements

Potential areas for extension:
- Chart visualizations (Recharts integration)
- Multiple file format support
- Report history/database storage
- User authentication
- Scheduled report generation
- Email delivery
- Custom KPI templates

