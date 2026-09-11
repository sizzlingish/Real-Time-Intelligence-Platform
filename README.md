# 🛰️ Real-Time Intelligence Platform

**Real-Time Intelligence Platform (RTIP)** is an AI-powered news intelligence system that retrieves current information from multiple news sources, analyzes the information using AI, and presents a concise, source-backed intelligence report.

## 🎯 Project Goal

News and information are scattered across many different sources. RTIP aims to bring relevant current information together and transform it into useful intelligence.

Instead of simply showing headlines, RTIP answers questions such as:

> "What is happening in Pakistan today?"

The platform retrieves relevant news, removes duplicate information, analyzes the available sources, and generates an AI-powered response.

---

## 🚀 Core Features

* 🔎 Search current news using a user question
* 📰 Retrieve articles from news APIs
* 🧹 Clean and remove duplicate articles
* 🎯 Retrieve the most relevant articles
* 🤖 Analyze retrieved information using Gemini
* ⚖️ Compare information across sources
* ⚠️ Identify conflicting information
* 📌 Explain why an event matters
* 🔗 Provide original news sources
* 🌐 Deploy as a web application using Streamlit

---

## 🧠 How RTIP Works

```text
User Question
      ↓
Streamlit Interface
      ↓
News APIs
      ↓
Article Collection
      ↓
Retrieval & Deduplication
      ↓
Relevant Articles
      ↓
Gemini AI
      ↓
Intelligence Analysis
      ↓
Streamlit Dashboard
```

---

## 🏗️ Project Structure

```text
Real-Time-Intelligence-Platform/
│
├── app.py
├── news_api.py
├── retrieval.py
├── ai.py
├── requirements.txt
├── README.md
└── .gitignore
```

### File Responsibilities

| File               | Purpose                                                  |
| ------------------ | -------------------------------------------------------- |
| `app.py`           | Streamlit user interface                                 |
| `news_api.py`      | Retrieves current news                                   |
| `retrieval.py`     | Cleans, deduplicates and ranks articles                  |
| `ai.py`            | Sends retrieved information to Gemini                    |
| `requirements.txt` | Python dependencies                                      |
| `README.md`        | Project documentation                                    |
| `.gitignore`       | Prevents sensitive/unnecessary files from being uploaded |

---

## 🛠️ Technology Stack

* **Python**
* **Streamlit**
* **NewsData.io**
* **Google Gemini**
* **Requests**
* **GitHub**
* **Streamlit Cloud**

---

## 🔐 Environment Variables

RTIP uses API keys that should not be stored directly in the source code.

Required keys:

```text
NEWSDATA_API_KEY
GEMINI_API_KEY
```

For local development, these should be provided through environment variables.

For deployment, they should be stored using Streamlit Secrets.

---

## 📦 Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd Real-Time-Intelligence-Platform
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

## 🌐 Deployment

RTIP can be deployed using Streamlit Cloud.

Deployment flow:

```text
GitHub Repository
       ↓
Streamlit Cloud
       ↓
Select app.py
       ↓
Configure Secrets
       ↓
Deploy
       ↓
Public RTIP Web Application
```

Streamlit automatically installs the dependencies listed in `requirements.txt`.

---

## 🔮 Future Improvements

Planned improvements include:

* Multiple news API sources
* Semantic/embedding-based retrieval
* Event clustering
* Timeline generation
* Source reliability analysis
* Confidence scoring
* "What changed?" detection
* Location-based intelligence
* Real-time alerts
* Interactive intelligence dashboard

---

## 🏆 Hackathon MVP

The initial MVP focuses on:

```text
Ask a question
      ↓
Retrieve current news
      ↓
Remove duplicates
      ↓
Select relevant information
      ↓
Analyze with AI
      ↓
Generate intelligence report
      ↓
Show sources
```

The goal is to demonstrate how scattered real-time news can be transformed into structured, understandable intelligence.

---

## 📄 Project Status

🚧 **Currently under development**

Real-Time Intelligence Platform is being developed as a hackathon project.
