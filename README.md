📘 PaperLens — AI Past Paper Analyzer

Analyze past papers → Identify high-yield topics → Generate a smart study plan.

🚀 Overview

PaperLens helps students prepare smarter by analyzing past exam papers and identifying the most important topics based on frequency and trends.

✨ Features
📄 Upload or use past papers (PDF)
🔍 Topic frequency analysis (based on syllabus)
📊 Visual charts (topic distribution)
🔥 High-priority & predicted topics
📅 Personalized study plan
🧠 OCR support for scanned PDFs
🛠 Tech Stack
Streamlit
Python
Plotly
pdfplumber
pytesseract (OCR)

⚙️ Setup
pip install -r requirements.txt
brew install tesseract poppler   # Mac only
streamlit run app.py

📁 Structure
app.py
utils/
papers_dataset/
syllabus_dsa.json

⚠️ Note
Works best with text-based PDFs. OCR is used for scanned files.

🎬 Demo
