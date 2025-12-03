# 🚀 GroundTruth Automated Insight Engine (GAIE) 

### *AI-Powered Automated Data → Insights → PDF Report Generator*  

**Built with React, Flask, Python (Pandas), Google Gemini API**

---

## ⭐ Why I Chose This Problem (H-001)

I chose the **Automated Insight Engine** challenge because it aligns perfectly with my strengths in:

- Python, Pandas, Data Analytics  
- React Frontend Engineering  
- Flask Backend Development  
- LLM-powered automation using Gemini  
- PDF programmatic generation  

The problem reflects a **real business workflow in AdTech** where analysts manually build weekly reports. Automating this process saves hours of repetitive work, making this solution both practical and impactful.

---

## 📌 Problem Statement — Real World Scenario

Marketing and AdTech companies generate massive daily datasets like:

- Foot traffic  
- Ad impressions & clicks  
- Weather & location data  
- Campaign logs  

Account managers manually:

- Download CSVs  
- Clean and merge data  
- Generate KPIs  
- Build charts  
- Write insights  
- Prepare PPT/PDF reports  

This is slow, repetitive, and error-prone.

**Goal:**  
✨ Build a system that automatically converts raw data → insights → downloadable PDF.

---

## 🎯 Solution Overview

The **GroundTruth Automated Insight Engine (GAIE)** automatically:

- Ingests CSV data  
- Cleans and preprocesses it  
- Calculates KPIs  
- Detects trends and anomalies  
- Generates correlation analysis  
- Uses **Gemini AI** to write insights, summaries, and recommendations  
- Exports everything into **PDF**  
- Includes a **chatbot** for querying dataset insights  

Fully automated end-to-end.

---

## 🧠 Expected End Result

Users receive:

- KPI Dashboard  
- Trend & anomaly analysis  
- AI-generated insights  
- Executive summary  
- Business recommendations  
- Downloadable PDF report  
- Interactive Gemini-powered analytics chatbot  

---

## 🏗️ Architecture

```
               ┌──────────────────────────┐
               │        React UI          │
               │ (Upload CSV, Display UI) │
               └─────────────┬────────────┘
                             │ Axios
                             ▼
               ┌──────────────────────────┐
               │        Flask API         │
               │  /upload /chat /export  │
               └─────────────┬────────────┘
                             │ Python
            ┌────────────────┴────────────────┐
            ▼                                 ▼
 ┌────────────────────┐              ┌───────────────────────┐
 │ Data Processing     │              │ Gemini LLM            │
 │ Pandas              │<─Prompts────│ Insights, Summary,     │
 │ Cleaning, KPIs      │              │ Recommendations        │
 └────────────────────┘              └───────────────────────┘
            │
            ▼
 ┌──────────────────────────┐
 │ Report (PDF Builder)     │
 │ ReportLab                │
 └─────────────┬────────────┘
               │
               ▼
    ┌────────────────────────┐
    │ Downloadable PDF       │
    └────────────────────────┘
```

---

## ⚙️ Tech Stack

### **Frontend**
- React 18  
- Material-UI  
- Axios  
- React-Dropzone  

### **Backend**
- Flask  
- Pandas  
- ReportLab (PDF Generation)  
- Flask-CORS  

### **AI**
- Google Gemini API  
- Custom Prompt Engineering  

### **Environment**
- Python 3.8+  
- Node.js 16+  

---

## 🧩 Features

- ✔ Automated ETL Pipeline  
- ✔ KPI Extraction (6-12 KPIs)  
- ✔ Trend Analysis  
- ✔ Anomaly Detection  
- ✔ Correlation Analysis  
- ✔ AI Insights (Gemini)  
- ✔ Executive Summary  
- ✔ PDF Export  
- ✔ Analytics Chatbot  
- ✔ Modern React Dashboard  

---

## 🖼️ Visual Proof

### Dashboard  
[ADD DASHBOARD IMAGE HERE]

### KPIs  
[ADD KPI CARDS IMAGE HERE]

### AI Insights  
[ADD INSIGHTS IMAGE HERE]

### Final PDF  
[ADD REPORT OUTPUT IMAGE HERE]

---

## 📤 Sample Output

### KPI Output (JSON)

```json
{
  "kpis": [
    "Total Impressions: 125,000",
    "Average CTR: 3.2%",
    "Top City: New York",
    "Best Day: 2024-02-21",
    "Conversion Rate: 2.5%",
    "ROAS: 4.2x"
  ]
}
```

### AI Insight

```
• CTR dropped by 12% this week due to reduced evening impressions.
• Hyderabad recorded a 24% improvement in conversions.
• Weekend traffic shows 34% higher engagement rates.
```

---

## 🔧 Installation & Setup

### Clone Project

```bash
git clone https://github.com/your-username/insight-engine.git
cd insight-engine
```

### Backend Setup (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Create .env (Optional)

```ini
GEMINI_API_KEY=YOUR_KEY_HERE
```

*Note: Currently configured in `backend/app.py`*

### Run Backend

```bash
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

### Windows Quick Start

Double-click `start.bat` to start both servers automatically.

---

## 🧠 Challenges Faced

- Handling messy CSV files with missing values
- Keeping LLM outputs structured (JSON parsing)
- Automating PDF generation with proper formatting
- Ensuring smooth React ↔ Flask communication
- Managing CORS between frontend and backend
- Prompt engineering for consistent analytics reports

---

## 📚 Learnings

- Building end-to-end ETL automation
- Prompt engineering for analytics insights
- React dashboard architecture with Material-UI
- PDF generation pipelines with ReportLab
- KPI engineering and insight writing
- Flask REST API design patterns
- Gemini API integration and response handling

---

## 🚀 Future Enhancements

- Multi-source ingestion (CSV + SQL + APIs)
- Scheduled automated weekly reports
- Multi-client dashboards
- Cloud deployment (Railway / Render / Vercel)
- PPTX export (python-pptx integration)
- Chart visualizations (Recharts)
- Vector database for insight memory
- Report history and versioning
- Email report delivery

---

## 🏁 Conclusion

The GroundTruth Automated Insight Engine automates:

- Data cleaning
- KPI generation
- Trend & anomaly detection
- Insight & summary writing
- PDF report building
- Interactive Q&A chatbot

This project demonstrates strong capabilities in AI, Data Engineering, Automation, and Full-Stack Development, making it highly suitable for real-world AdTech reporting workflows.

---

## 📄 License

MIT License

## 🤝 Support

For issues or questions, please open an issue on the repository.
