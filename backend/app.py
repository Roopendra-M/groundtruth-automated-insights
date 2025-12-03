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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from dotenv import load_dotenv

# --------------------------------------------------------
# INITIAL SETUP
# --------------------------------------------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

load_dotenv()  # Load .env file

# --------------------------------------------------------
# GEMINI CONFIG
# --------------------------------------------------------

# The Google SDK requires GOOGLE_API_KEY
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

API_KEY = GOOGLE_KEY or GEMINI_KEY

if not API_KEY:
    raise RuntimeError("ERROR: No API key found! Add GOOGLE_API_KEY=... to your .env")

print("DEBUG: Loaded API Key:", API_KEY[:10] + "*********")

genai.configure(api_key=API_KEY)

# SAFE WORKING MODELS
GEMINI_MODEL_ID = "gemini-2.5-pro"


# --------------------------------------------------------
# HELPERS
# --------------------------------------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def analyze_dataframe(df):
    """Extract summary for LLM prompt"""
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": df.describe().to_dict()
        if len(df.select_dtypes(include=["number"]).columns) > 0
        else {},
        "sample_rows": df.head(5).to_dict("records")
    }


# --------------------------------------------------------
# FALLBACK – If Gemini fails
# --------------------------------------------------------

def generate_basic_report(summary):
    total_rows = summary["total_rows"]
    total_columns = summary["total_columns"]
    numeric_summary = summary.get("numeric_summary", {})
    
    kpis = [f"Total rows: {total_rows}", f"Total columns: {total_columns}"]

    for col, stats in list(numeric_summary.items())[:4]:
        if stats.get("mean") is not None:
            kpis.append(f"Average {col}: {round(stats['mean'], 2)}")

    return {
        "data_understanding": f"Dataset has {total_rows} rows and {total_columns} columns.",
        "kpis": kpis,
        "trend_analysis": "Trend analysis unavailable (fallback mode).",
        "anomaly_detection": "Anomaly detection unavailable (fallback mode).",
        "correlation_analysis": "Correlation unavailable (fallback mode).",
        "insights": ["Insight generation unavailable in fallback mode."],
        "executive_summary": "Fallback summary – no AI response.",
        "business_recommendations": ["Re-run when AI is available."],
        "slide_deck": {},
        "chatbot_format": {}
    }


# --------------------------------------------------------
# GEMINI REPORT GENERATOR
# --------------------------------------------------------

def generate_report_with_gemini(summary, columns, sample):
    prompt = f"""
You are an expert data analyst. Based ONLY on this dataset summary, generate a full analytics report.

SUMMARY:
{json.dumps(summary, indent=2)}

COLUMNS:
{columns}

SAMPLE ROWS:
{json.dumps(sample[:3], indent=2)}

Return ONLY JSON:
{{
  "data_understanding": "",
  "kpis": [],
  "trend_analysis": "",
  "anomaly_detection": "",
  "correlation_analysis": "",
  "insights": [],
  "executive_summary": "",
  "business_recommendations": [],
  "slide_deck": {{
    "slide_1_title": "",
    "slide_2_kpis": [],
    "slide_3_charts": "",
    "slide_4_insights": [],
    "slide_5_anomalies": [],
    "slide_6_recommendations": [],
    "slide_7_summary": ""
  }},
  "chatbot_format": {{
    "kpis": [],
    "insights": [],
    "summary": "",
    "recommendations": [],
    "anomalies": [],
    "chart_explanations": [],
    "trend_analysis": "",
    "columns": [],
    "chatbot_memory": {{
      "dataset_summary": "",
      "kpis": [],
      "insights": []
    }}
  }}
}}
"""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_ID)
        response = model.generate_content(prompt)

        text = response.text

        # Extract JSON
        first = text.find("{")
        last = text.rfind("}")
        clean_json = text[first:last + 1]

        return json.loads(clean_json)

    except Exception as e:
        print("AI ERROR:", e)
        return generate_basic_report(summary)


# --------------------------------------------------------
# ROUTES
# --------------------------------------------------------

@app.route("/api/health")
def health():
    return jsonify({"status": "running", "model": GEMINI_MODEL_ID})


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only CSV allowed"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    summary = analyze_dataframe(df)

    report = generate_report_with_gemini(
        summary,
        summary["column_names"],
        summary["sample_rows"]
    )

    report["metadata"] = {
        "filename": filename,
        "timestamp": datetime.now().isoformat(),
        "rows": summary["total_rows"],
        "columns": summary["total_columns"],
        "model_used": GEMINI_MODEL_ID
    }

    return jsonify(report)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question")
    context = data.get("context", {})

    prompt = f"""
Answer this question based ONLY on this context:
{json.dumps(context, indent=2)}

Question: {question}
"""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_ID)
        res = model.generate_content(prompt)
        return jsonify({"answer": res.text})
    except:
        return jsonify({"answer": "AI unavailable"})


# --------------------------------------------------------
# EXPORT PDF
# --------------------------------------------------------

@app.route("/api/export/pdf", methods=["POST"])
def export_pdf():
    data = request.json

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    def add_section(title, content):
        story.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
        if isinstance(content, list):
            for c in content:
                story.append(Paragraph(f"• {c}", styles["Normal"]))
        else:
            story.append(Paragraph(str(content), styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Weekly Analytics Report</b>", styles["Title"]))

    add_section("Executive Summary", data.get("executive_summary", ""))
    add_section("KPIs", data.get("kpis", []))
    add_section("Insights", data.get("insights", []))
    add_section("Recommendations", data.get("business_recommendations", []))

    doc.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        download_name="analytics_report.pdf",
        as_attachment=True,
        mimetype="application/pdf"
    )


# --------------------------------------------------------
# RUN
# --------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
