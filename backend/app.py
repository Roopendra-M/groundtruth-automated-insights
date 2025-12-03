from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import json
import os
from datetime import datetime
import google.generativeai as genai
from werkzeug.utils import secure_filename
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBc6u-l2cT21ckh-kQ30sbSxB7vaZdXQkQ")
GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-pro")
genai.configure(api_key=GEMINI_API_KEY)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_dataframe(df):
    """Extract summary statistics from dataframe"""
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'column_names': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
        # Limit sample rows to keep LLM prompt compact
        'sample_rows': df.head(5).to_dict('records')
    }
    return summary

def generate_basic_report(summary):
    """Fallback: generate a simple report without calling Gemini (no LLM, no external API)."""
    total_rows = summary.get("total_rows", 0)
    total_columns = summary.get("total_columns", 0)
    column_names = summary.get("column_names", [])
    numeric_summary = summary.get("numeric_summary", {})

    # Build a few simple KPIs from numeric columns
    kpis = [f"Total rows: {total_rows}", f"Total columns: {total_columns}"]
    for col, stats in list(numeric_summary.items())[:4]:
        mean_val = stats.get("mean")
        if mean_val is not None:
            kpis.append(f"Average {col}: {round(mean_val, 2)}")

    data_understanding = (
        f"This dataset has {total_rows} rows and {total_columns} columns. "
        f"Columns available: {', '.join(column_names[:10])}"
        + (" ..." if len(column_names) > 10 else "")
    )

    trend_analysis = (
        "Trend analysis is limited because only aggregate summary statistics were used; "
        "time-based patterns cannot be inferred without inspecting a date/time column directly."
    )

    anomaly_detection = (
        "Anomaly detection is not available in the offline fallback mode. "
        "Consider re-running when the Gemini service is reachable for deeper anomaly insights."
    )

    correlation_analysis = (
        "Correlation analysis is not computed in this fallback mode. "
        "Only basic univariate statistics (e.g., means) were derived from numeric columns."
    )

    insights = [
        "The dataset was successfully ingested and basic structural statistics were computed locally.",
        "More advanced narrative insights and correlations require the Gemini service to be available.",
    ]

    executive_summary = (
        "Due to connectivity or timeout issues with the Gemini API, this report was generated using a "
        "lightweight offline fallback. The dataset’s structure and basic statistics were successfully "
        "computed, including row and column counts and average values for key numeric fields. However, "
        "advanced narrative analytics—such as natural-language insights, anomaly explanations, and detailed "
        "trend narratives—are not included here. For a full AI-written executive report with deeper marketing "
        "and AdTech insights, please re-run the analysis once the Gemini service is responsive."
    )

    business_recommendations = [
        "Re-run the analysis when the Gemini model is responsive to obtain a full narrative report.",
        "Use the basic KPIs (row counts and averages) as a quick data quality and volume check.",
        "Verify that the dataset includes a clear date/time column to enable trend and week-over-week analysis.",
        "Ensure key performance fields (impressions, clicks, conversions, revenue) are numeric and non-null.",
        "If needed, filter or sample the dataset to a shorter time window to reduce processing time.",
        "Log and monitor any repeated timeout issues to adjust model choice or prompt size.",
    ]

    slide_deck = {
        "slide_1_title": "Weekly Analytics Report (Fallback Mode)",
        "slide_2_kpis": kpis,
        "slide_3_charts": "Basic numeric KPIs only; no AI-generated charts in fallback mode.",
        "slide_4_insights": insights,
        "slide_5_anomalies": ["Anomaly and outlier analysis not available in fallback mode."],
        "slide_6_recommendations": business_recommendations,
        "slide_7_summary": "Offline fallback summary based on structural dataset statistics only.",
    }

    chatbot_format = {
        "kpis": kpis,
        "insights": insights,
        "summary": executive_summary,
        "recommendations": business_recommendations,
        "anomalies": [anomaly_detection],
        "chart_explanations": ["Only basic KPIs are available; no AI-generated charts."],
        "trend_analysis": trend_analysis,
        "columns": column_names,
        "chatbot_memory": {
            "dataset_summary": json.dumps(summary, indent=2),
            "kpis": kpis,
            "insights": insights,
        },
    }

    return {
        "data_understanding": data_understanding,
        "kpis": kpis,
        "trend_analysis": trend_analysis,
        "anomaly_detection": anomaly_detection,
        "correlation_analysis": correlation_analysis,
        "insights": insights,
        "executive_summary": executive_summary,
        "business_recommendations": business_recommendations,
        "slide_deck": slide_deck,
        "chatbot_format": chatbot_format,
    }

def generate_report_with_gemini(summary, columns, sample):
    """Generate comprehensive analytics report using Gemini"""

    # Use a compact version of the summary to avoid huge prompts (reduces timeout risk)
    summary_for_llm = dict(summary)
    # Remove raw sample rows from the summary block (they are passed separately)
    summary_for_llm.pop("sample_rows", None)

    prompt = f"""You are an expert Data Analyst + Business Intelligence Specialist + Report Writer.
Your job is to take an uploaded dataset (CSV) and generate a FULL weekly analytics report
for a marketing/ad-tech use case.

Below is the dataset summary and column information:

DATA SUMMARY:
{json.dumps(summary_for_llm, indent=2)}

COLUMN NAMES:
{columns}

RAW SAMPLE ROWS:
{json.dumps(sample[:3], indent=2)}

-----------------------------------------
YOUR TASKS (Follow EXACTLY in this order)
-----------------------------------------

## 1. DATA UNDERSTANDING
Explain:
- What type of dataset this is
- What each column likely represents
- Time period (if date/time exists)
- Data completeness & quality
- Any missing or unusual patterns

Make this section short and clear.

## 2. KPI GENERATION
Generate 6–12 KPIs based ONLY on provided dataset.

Examples of KPIs you may include:
- Total visitors / impressions / clicks
- Average CTR
- Conversion rate
- Top performing cities / locations
- Best & worst performing days
- Growth or decline percentages
- Correlation-based KPIs (e.g., "Rainy days → 12% drop in footfall")

Include exact values, formatted cleanly.
No hallucinations — use only provided data summary.

## 3. TREND ANALYSIS
Explain clear trends:
- Increasing/decreasing patterns
- Seasonal or weekday patterns
- Peak times or dates
- Spikes or drops & the likely reasons
- Category-wise insights (city, region, device, etc.)

Write this like a BI dashboard analyst.

## 4. ANOMALY DETECTION
Identify anomalies such as:
- Sudden spikes
- Unexpected drops
- Missing values
- Outliers
- Sharp changes in performance

Explain why they might have happened.

## 5. CORRELATION ANALYSIS
Explain relationships:
- Weather ↔ Sales
- Foot traffic ↔ Clickthrough rate
- Day-of-week ↔ Conversions
- City ↔ Performance
- Time-of-day ↔ Engagement

Only state real patterns supported by the data.

## 6. INSIGHTS (MOST IMPORTANT)
Generate strong insights that senior leaders care about.  
Cover:
- What improved this week?
- What dropped?
- What caused the changes?
- What the business should pay attention to

Write in crisp bullet points.

## 7. EXECUTIVE SUMMARY (150–200 words)
Write a polished leadership-friendly summary including:
- Overall performance
- High-level trends
- Critical insights
- Key takeaways
- A short narrative of what this week looked like

## 8. BUSINESS RECOMMENDATIONS
Generate 6 highly actionable recommendations.
Each must be:
- Specific
- Measurable
- Data-driven
- Tied to KPIs
- Relevant for AdTech / Retail analytics

Example:
"Increase ad spend by 20% on weekends where traffic is 34% higher."

## 9. SLIDE DECK / PDF CONTENT (Structured)
Return content for:
### Slide 1: Title Page
- Week Number
- Campaign/Client Name
- Analyst: AI Insight Engine

### Slide 2: KPIs
Bullet list of KPIs.

### Slide 3: Charts & Visuals
Describe which charts should be included:
- Line graph for daily trend
- Bar chart for category comparison
- Heatmap for correlations

### Slide 4: Insights
Short bullet list.

### Slide 5: Anomalies
Short bullet list.

### Slide 6: Recommendations
Numbered list.

### Slide 7: Final Summary
Concise leadership message.

## 10. CHATBOT ANSWERING FORMAT
Also prepare content in a JSON-friendly structure like:

{{
  "kpis": [...],
  "insights": [...],
  "summary": "...",
  "recommendations": [...],
  "anomalies": [...],
  "chart_explanations": [...],
  "trend_analysis": [...],
  "columns": [...],
  "chatbot_memory": {{
       "dataset_summary": "{json.dumps(summary, indent=2)}",
       "kpis": [...],
       "insights": [...]
  }}
}}

This will help with chatbot Q&A feature.

-----------------------------------------
IMPORTANT RULES:
-----------------------------------------
- DO NOT hallucinate data.
- Use ONLY the columns & summary provided.
- Keep tone professional & executive-ready.
- Use numbers, percentages, references to dates when available.
- Be precise, confident, and insightful.

Return your response in JSON format with the following structure:
{{
  "data_understanding": "...",
  "kpis": [...],
  "trend_analysis": "...",
  "anomaly_detection": "...",
  "correlation_analysis": "...",
  "insights": [...],
  "executive_summary": "...",
  "business_recommendations": [...],
  "slide_deck": {{
    "slide_1_title": "...",
    "slide_2_kpis": [...],
    "slide_3_charts": "...",
    "slide_4_insights": [...],
    "slide_5_anomalies": [...],
    "slide_6_recommendations": [...],
    "slide_7_summary": "..."
  }},
  "chatbot_format": {{
    "kpis": [...],
    "insights": [...],
    "summary": "...",
    "recommendations": [...],
    "anomalies": [...],
    "chart_explanations": [...],
    "trend_analysis": "...",
    "columns": [...],
    "chatbot_memory": {{
      "dataset_summary": "...",
      "kpis": [...],
      "insights": [...]
    }}
  }}
}}
"""
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_ID)
        response = model.generate_content(prompt)
        
        # Try to parse JSON from response
        response_text = response.text
        
        # Clean up the response text to extract JSON
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            if json_end == -1:
                json_end = len(response_text)
            response_text = response_text[json_start:json_end].strip()
        
        # Try to find JSON object in the text
        if '{' in response_text:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            response_text = response_text[json_start:json_end]
        
        report_data = json.loads(response_text)
        return report_data
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return a structured error with the raw response
        return {
            "error": f"Error parsing AI response as JSON: {str(e)}",
            "raw_response": response.text if 'response' in locals() else None,
            "fallback_message": "The AI generated a response but it wasn't in the expected JSON format. Please try again."
        }
    except Exception as e:
        # On timeout or other Gemini failures, fall back to a basic local report
        if "504" in str(e) or "timed out" in str(e).lower():
            return generate_basic_report(summary)
        return {
            "error": f"Error generating report: {str(e)}",
            "raw_response": response.text if 'response' in locals() else None
        }

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Analytics Report API is running"})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            
            # Analyze dataframe
            summary = analyze_dataframe(df)
            
            # Generate report
            report = generate_report_with_gemini(
                summary,
                summary['column_names'],
                summary['sample_rows']
            )
            
            if isinstance(report, dict) and report.get("error"):
                app.logger.error("Report generation failed: %s", report.get("error"))
                return jsonify(report), 500
            
            # Add metadata
            report['metadata'] = {
                'filename': filename,
                'upload_date': datetime.now().isoformat(),
                'total_rows': summary['total_rows'],
                'total_columns': summary['total_columns']
            }
            
            return jsonify(report)
            
        except Exception as e:
            app.logger.exception("Upload processing failed")
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Only CSV files are allowed."}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chatbot endpoint for Q&A about the report"""
    data = request.json
    question = data.get('question', '')
    context = data.get('context', {})
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    prompt = f"""You are a helpful analytics assistant. Answer the following question about the analytics report.

Context from the report:
{json.dumps(context, indent=2)}

Question: {question}

Provide a clear, concise, and data-driven answer based on the report context. If the question cannot be answered from the provided context, say so."""
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_ID)
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        app.logger.exception("Chat endpoint failed")
        return jsonify({"error": f"Error generating answer: {str(e)}"}), 500

@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Export report as PDF"""
    data = request.json
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1a1a1a',
        spaceAfter=30
    )
    story.append(Paragraph("Weekly Analytics Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Paragraph(data.get('executive_summary', ''), styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # KPIs
    story.append(Paragraph("Key Performance Indicators", styles['Heading2']))
    kpis = data.get('kpis', [])
    for kpi in kpis:
        story.append(Paragraph(f"• {kpi}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Insights
    story.append(Paragraph("Key Insights", styles['Heading2']))
    insights = data.get('insights', [])
    for insight in insights:
        story.append(Paragraph(f"• {insight}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    story.append(Paragraph("Business Recommendations", styles['Heading2']))
    recommendations = data.get('business_recommendations', [])
    for i, rec in enumerate(recommendations, 1):
        story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)

