# AI Company Brochure Generator

An AI-powered application that automatically creates professional company brochures from website URLs using Python, Streamlit, and Ollama.

## Project Overview

The AI Company Brochure Generator takes a company website URL, extracts relevant information from multiple website pages, and uses a local Large Language Model (LLM) to generate brochure content.

The generated content is converted into a professionally styled HTML page and downloadable PDF.

## Features

- Enter a company website URL.
- Scrape relevant information from multiple website pages.
- Identify About, Services, Products, and Contact pages.
- Generate brochure content using Ollama.
- Convert Markdown content into styled HTML.
- Generate downloadable PDF brochures.
- Simple and interactive Streamlit interface.

## Technologies Used

- Python
- Streamlit
- Ollama
- Qwen 3.5 4B
- BeautifulSoup
- Requests
- Playwright
- HTML
- CSS

## Project Structure

```text
AI-Brochure-Generator/
├── ai/
├── brochure/
├── pdf/
├── scraper/
├── utils/
├── app.py
├── requirements.txt
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shaikfarzana2004-sketch/AI-Brochure-Generator.git
```

### 2. Navigate to the project folder

```bash
cd AI-Brochure-Generator
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Ollama model

Install Ollama and download the model:

```bash
ollama pull qwen3.5:4b
```

Make sure Ollama is running before starting the application.

### 7. Run the application

```bash
streamlit run app.py
```

Open the local URL shown in your terminal, usually:

`http://localhost:8501`

## How to Use

1. Start the Streamlit application.
2. Enter a company website URL.
3. Click the Generate Brochure button.
4. Wait while the application scrapes website information and generates content.
5. View the generated brochure.
6. Download the brochure as a PDF.

## Output

The application generates a professionally styled company brochure in PDF format.

## Author

**Shaik Farzana**

GitHub: https://github.com/shaikfarzana2004-sketch
