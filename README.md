# 📘 PaperLens – AI Past Paper Analyzer & Smart Study Planner

> *Focus on what matters. Ace the exam.*

A simple, fast, and beautiful web application that analyzes past exam papers, identifies high-priority topics, and generates a smart personalized study plan.

---

## 🎯 Features

| Feature | Description |
|---|---|
| 📄 PDF Extraction | Reads all past papers from `papers_dataset/` automatically |
| 🔍 Topic Detection | Keyword-matches syllabus topics against extracted text |
| 📊 Frequency Analysis | Bar & pie charts showing topic importance |
| 🔥 Insights | Top, low-priority, and predicted topics |
| 🔮 Prediction | Flags under-asked topics likely to appear next |
| 📅 Study Planner | Day-by-day plan based on your available time |

---

## 📂 Project Structure

```
past-paper-analyzer/
├── app.py                  ← Main Streamlit application
├── syllabus.json           ← Subject syllabus (edit to match your subject)
├── papers_dataset/
│   ├── cse1.pdf            ← Past paper 1
│   ├── cse2.pdf
│   ├── cse3.pdf
│   ├── cse4.pdf
│   └── cse5.pdf
├── utils/
│   ├── extractor.py        ← PDF text extraction
│   ├── analyzer.py         ← Topic analysis & ranking
│   └── planner.py          ← Study plan generation
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your PDFs
Place your past exam papers (PDF format) into the `papers_dataset/` folder.

### 3. Edit the syllabus
Open `syllabus.json` and update it to match your subject:

```json
{
  "Unit 1: Linear Data Structures": ["Arrays", "Linked List"],
  "Unit 2: Stack & Queue": ["Stacks", "Queues"],
  "Unit 3: Trees": ["Trees", "Binary Tree", "BST"],
  "Unit 4: Graphs": ["Graphs", "BFS", "DFS"],
  "Unit 5: Sorting": ["Sorting", "Searching", "Quick Sort"]
}
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this project to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file** to `app.py`
5. Click **Deploy**

Your app will be live at a public URL instantly.

---

## 🛠 Tech Stack

- **[Streamlit](https://streamlit.io)** – Frontend + server
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** – PDF text extraction
- **[Plotly](https://plotly.com/python/)** – Interactive charts
- **[Pandas](https://pandas.pydata.org/)** – Data handling
- **JSON** – Syllabus format

---

## 🎬 Demo Flow

1. Open the sidebar → set **Days left** and **Study hours/day**
2. Click **🚀 Run Analysis**
3. View topic frequency bar & pie charts
4. Check **Insights** – top, low-priority, and predicted topics
5. Scroll to your **personalized study plan**

---

## ⚠️ Constraints & Design Decisions

- No ML models – pure keyword frequency analysis
- No external APIs required
- Works entirely offline after installation
- Simple, clean, and fast

---

*"This tool helps students focus only on high-impact topics and saves hours of manual analysis."*
