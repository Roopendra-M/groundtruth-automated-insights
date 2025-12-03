# Quick Start Guide

Get your AI-Powered Analytics Report Generator up and running in minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Step 1: Backend Setup

1. Open a terminal and navigate to the backend folder:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. (Optional) Generate sample data for testing:
```bash
python generate_sample_data.py
```

6. Start the backend server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

## Step 2: Frontend Setup

1. Open a **new terminal** and navigate to the frontend folder:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the frontend development server:
```bash
npm start
```

The frontend will automatically open in your browser at `http://localhost:3000`

## Step 3: Using the Application

1. **Upload a CSV file**:
   - Click on the "Upload" tab
   - Drag and drop a CSV file or click to browse
   - Wait for the AI to analyze your data (this may take 30-60 seconds)

2. **View your report**:
   - The report will automatically appear in the "Report" tab
   - Explore different sections using the expandable accordions
   - Click "Export PDF" to download a PDF version

3. **Chat with the assistant**:
   - Go to the "Chat" tab
   - Ask questions like:
     - "What are the top KPIs?"
     - "What insights should I focus on?"
     - "Are there any anomalies?"
     - "What are the main recommendations?"

## Windows Quick Start (One-Click)

If you're on Windows, you can use the provided batch files:

1. **Start both servers**: Double-click `start.bat`
   - This will open two command windows (backend and frontend)

2. **Or start individually**:
   - `start_backend.bat` - Backend only
   - `start_frontend.bat` - Frontend only

## Sample Data

If you need sample data to test with:

1. Run the sample data generator:
```bash
cd backend
python generate_sample_data.py
```

2. This creates `sample_marketing_data.csv` in the backend folder

3. Upload this file through the web interface

## Troubleshooting

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Check if port 5000 is already in use
- Verify all dependencies are installed: `pip list`

### Frontend won't start
- Make sure Node.js is installed: `node --version`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 3000 is already in use

### API errors
- Verify the Gemini API key is correct in `backend/app.py`
- Check your internet connection (Gemini API requires internet)
- Look at the backend console for detailed error messages

### File upload issues
- Ensure your CSV file is under 16MB
- Check that the file is a valid CSV format
- Make sure the file has headers in the first row

## Next Steps

- Customize the report template in `backend/app.py`
- Add more visualizations in `frontend/src/components/ReportViewer.js`
- Extend the chatbot with more context in `backend/app.py` (chat endpoint)

## Support

If you encounter any issues:
1. Check the console/terminal for error messages
2. Verify all dependencies are installed
3. Ensure both servers are running
4. Check that your CSV file is properly formatted

Happy analyzing! 📊

