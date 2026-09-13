# 🛰️ Real-Time Intelligence Platform (RTIP)

**Real-Time Intelligence Platform (RTIP)** is an AI-powered intelligence dashboard that combines **real-time news retrieval, weather information, intelligent article retrieval, AI analysis, and source-backed reporting** in a single Streamlit application.

Instead of relying only on an AI model's existing knowledge, RTIP retrieves current information from external sources, processes the retrieved content, and uses AI to generate useful intelligence based on that information.

---

## 🎯 Project Goal

Information is constantly changing and is distributed across many different sources.

RTIP aims to transform this scattered information into **structured, understandable, and useful intelligence**.

Users can ask natural-language questions such as:

> "What are the latest technology developments?"

or:

> "What are the biggest global challenges facing the world right now?"

RTIP then searches for relevant current information, removes duplicate articles, ranks the most relevant results, and uses Gemini to analyze the retrieved information.

The platform also supports real-time weather queries such as:

> "Forecast in Islamabad"

---

# 🚀 Core Features

### 📰 Real-Time News Intelligence

* Search current news using natural-language questions
* Retrieve news from multiple news APIs
* Combine results from different sources
* Clean and normalize search queries
* Remove duplicate articles
* Rank articles based on relevance
* Select the most useful articles for analysis

### 🤖 AI-Powered Analysis

RTIP provides three answer modes:

* ⚡ **Smart Concise Intelligence** — short and direct answers
* 📄 **Detailed Intelligence Report** — structured analysis with key developments and context
* 🔬 **Advanced Research** — deeper research-style analysis, comparisons, different perspectives, implications, and critical analysis

### ⚖️ Source Comparison

The AI analyzes information from multiple retrieved articles and can:

* Compare information across sources
* Identify areas of agreement
* Identify conflicting claims
* Highlight missing or uncertain information
* Explain why an event or development matters

### 🌤️ Real-Time Weather

RTIP also provides weather information using Open-Meteo.

Users can ask questions such as:

* "Forecast in Islamabad"
* "Is it cold in London?"
* "What is the weather in America?"

The system detects weather-related questions and retrieves current weather information separately from the news pipeline.

### 📊 Visual Intelligence

When meaningful visualization can be generated from the retrieved information, RTIP can display relevant visual intelligence.

The system avoids forcing charts when the available information does not support a meaningful visualization.

### 🔗 Source-Backed Results

Generated intelligence is accompanied by the original news sources used by the system.

This allows users to inspect the information behind the generated answer.

---

# 🧠 How RTIP Works

RTIP separates **information retrieval** from **AI reasoning**.

```text
                         USER QUESTION
                              │
                              ▼
                    ┌──────────────────┐
                    │ Streamlit UI     │
                    └────────┬─────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
          WEATHER QUERY             NEWS QUERY
                 │                       │
                 ▼                       ▼
           Open-Meteo              Query Cleaner
                 │                       │
                 ▼                ┌──────┴──────┐
          Weather Answer           ▼             ▼
                              NewsData.io      GNews
                                   │             │
                                   └──────┬──────┘
                                          ▼
                                  Article Collection
                                          │
                                          ▼
                                  Deduplication
                                          │
                                          ▼
                                  Relevance Ranking
                                          │
                                          ▼
                                  Relevant Articles
                                          │
                                          ▼
                                    Gemini AI
                                          │
                         ┌────────────────┼────────────────┐
                         ▼                ▼                ▼
                      Concise          Detailed        Advanced
                         │                │                │
                         └────────────────┼────────────────┘
                                          ▼
                                  Intelligence Report
                                          │
                                          ▼
                                  Visualization
                                          │
                                          ▼
                                       Sources
```

---

# 🔍 Query Processing

Users naturally ask questions in conversational language.

For example:

> "What are the biggest risks and benefits of artificial intelligence for jobs, and do recent reports suggest AI will create more jobs than it replaces?"

News APIs generally work better with shorter search-oriented queries.

RTIP therefore creates a separate **API-friendly search query** while preserving the original user question.

```text
Original Question
       ↓
Query Cleaning
       ↓
Short Search Query
       ↓
News APIs
```

The **original question is preserved** for relevance ranking and AI analysis.

This allows RTIP to combine natural-language interaction with more effective news retrieval.

---

# 📰 News Retrieval Pipeline

RTIP retrieves articles from multiple news providers.

The current pipeline uses:

* **NewsData.io**
* **GNews**

The results are combined and passed through the retrieval layer.

```text
NewsData.io ──┐
              ├──→ Combined Articles
GNews ────────┘
                    ↓
              Deduplication
                    ↓
             Relevance Ranking
                    ↓
             Selected Articles
```

---

# 🧹 Retrieval & Deduplication

The retrieval system performs several processing steps.

### 1. Text Cleaning

Article text and user questions are normalized by:

* Converting text to lowercase
* Removing unnecessary punctuation
* Normalizing whitespace

### 2. Duplicate Detection

Articles with the same URL are removed.

Articles with highly similar titles are also identified and filtered.

### 3. Relevance Ranking

Articles are scored according to how closely their title and description relate to the user's original question.

The highest-ranked articles are selected for AI analysis.

---

# 🤖 AI Intelligence Engine

RTIP uses **Google Gemini** to analyze the retrieved articles.

The AI does not receive the user's question alone.

Instead, it receives:

```text
User Question
      +
Retrieved Relevant Articles
      ↓
Gemini
      ↓
Intelligence Analysis
```

This allows the generated response to be grounded in the current information retrieved by the platform.

---

# 📋 Answer Modes

## ⚡ Smart Concise Intelligence

Designed for quick answers.

The system produces a short response containing the most important information.

Useful when the user wants a quick overview without a long report.

---

## 📄 Detailed Intelligence Report

Provides a structured report containing areas such as:

* Intelligence Summary
* Key Developments
* Source Comparison
* Why It Matters
* Latest Information

This mode is useful when the user wants more context and explanation.

---

## 🔬 Advanced Research

Designed for challenging questions that require deeper analysis.

The research response can cover:

* Direct answer
* Introduction
* Background and context
* Detailed explanation
* Causes and contributing factors
* Effects and consequences
* Recent evidence
* Different perspectives
* Comparisons
* Critical analysis
* Advantages and disadvantages
* Real-world examples
* Future implications
* Conclusion
* Sources

The system is instructed to distinguish between **reported facts and analysis** and to identify uncertainty or conflicting information rather than presenting unsupported claims as facts.

---

# 🌤️ Weather Intelligence

Weather questions are detected separately from news questions.

```text
User Question
      ↓
Weather Detection
      ↓
Location Extraction
      ↓
Open-Meteo
      ↓
Current Weather Data
      ↓
Natural-Language Answer
```

The platform can retrieve information such as:

* Temperature
* Relative humidity
* Wind speed
* Weather conditions

Location names are automatically extracted from natural-language questions.

---

# 📊 Visualization

After generating intelligence, RTIP checks whether the retrieved information can support meaningful visualizations.

The system can generate relevant visual intelligence when appropriate.

However, **visualizations are not forced** when the available information is insufficient.

This prevents the system from creating misleading or unsupported charts.

---

# 🖥️ User Interface

The application is built using **Streamlit**.

The sidebar allows users to configure:

### News Search Location

Examples:

* No specific location
* Worldwide
* Pakistan
* India
* US
* UK
* China
* Hyderabad
* Karachi
* Islamabad

### Topic

Examples:

* All Topics
* AI
* Technology
* Politics
* Business
* Education
* Health
* Sports
* Climate
* Cybersecurity
* World News

### Answer Mode

* ⚡ Smart Concise Intelligence
* 📄 Detailed Intelligence Report
* 🔬 Advanced Research

### Article Limit

Users can also control how many articles are retrieved and analyzed.

---

# 🏗️ Project Structure

```text
Real-Time-Intelligence-Platform/
│
├── app.py
├── news_api.py
├── gnews_api.py
├── open_meteo_api.py
├── retrieval.py
├── ai.py
├── visualization.py
├── requirements.txt
├── README.md
└── .gitignore
```

## File Responsibilities

| File                | Purpose                                                              |
| ------------------- | -------------------------------------------------------------------- |
| `app.py`            | Main Streamlit application and user interface                        |
| `news_api.py`       | Retrieves and normalizes NewsData.io articles                        |
| `gnews_api.py`      | Retrieves and normalizes GNews articles                              |
| `open_meteo_api.py` | Location geocoding and weather retrieval                             |
| `retrieval.py`      | Text cleaning, deduplication, relevance scoring, and article ranking |
| `ai.py`             | Gemini prompts and AI-powered intelligence generation                |
| `visualization.py`  | Generates meaningful visual intelligence from retrieved information  |
| `requirements.txt`  | Python dependencies                                                  |
| `README.md`         | Project documentation                                                |
| `.gitignore`        | Prevents sensitive and unnecessary files from being committed        |

---

# 🛠️ Technology Stack

* **Python**
* **Streamlit**
* **Google Gemini**
* **NewsData.io**
* **GNews**
* **Open-Meteo**
* **Requests**
* **GitHub**
* **Streamlit Cloud**

---

# 🔐 API Keys & Secrets

RTIP uses API keys that should **never be hard-coded into the source code**.

Required credentials include:

```text
NEWSDATA_API_KEY
GEMINI_API_KEY
```

For local development, API keys can be provided through environment variables or the appropriate local secrets configuration.

For Streamlit deployment, sensitive credentials should be stored using **Streamlit Secrets**.

Do not commit API keys to GitHub.

---

# 📦 Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd Real-Time-Intelligence-Platform
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure the required API keys.

Then run the application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🌐 Deployment

RTIP can be deployed using Streamlit Cloud.

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
Public RTIP Application
```

Streamlit Cloud installs the dependencies specified in `requirements.txt`.

---

# 🧪 Example Questions

### Weather

```text
Forecast in Islamabad
```

```text
Is it cold in London?
```

```text
What is the weather in America?
```

### Worldwide + AI

```text
What is the news about AI?
```

### Business + US

```text
What are the latest business trends?
```

### Technology + China

```text
What are the latest technology developments?
```

### All Topics + Worldwide

```text
What are the biggest global challenges facing the world right now?
```

---

# 🏆 Hackathon MVP

The core MVP follows this pipeline:

```text
Ask a Question
       ↓
Clean Search Query
       ↓
Retrieve Current News
       ↓
Combine Multiple Sources
       ↓
Remove Duplicates
       ↓
Rank Relevant Articles
       ↓
Analyze With Gemini
       ↓
Generate Intelligence
       ↓
Visualize When Appropriate
       ↓
Show Original Sources
```

The MVP demonstrates how **real-time information from multiple sources can be transformed into structured AI-powered intelligence**.

---

# 🔮 Future Improvements

Potential future improvements include:

* Semantic / embedding-based retrieval
* Event clustering
* Timeline generation
* Source reliability scoring
* Confidence scoring
* "What changed?" detection
* Location-based intelligence
* Real-time alerts
* More news providers
* Advanced source comparison
* Interactive intelligence dashboards
* Historical event tracking
* Automated trend detection

---

# 📌 Project Status

🚧 **Currently under development**

RTIP is being developed as a **hackathon project** focused on demonstrating how real-time information retrieval, intelligent retrieval, and generative AI can work together to produce useful intelligence.

---

## 💡 Core Idea

> **Retrieve → Filter → Rank → Analyze → Visualize → Verify**

RTIP is designed to move beyond simply displaying news headlines and instead turn current information into **structured, understandable, and source-backed intelligence**.
