# 🎥 ViralCheck — YouTube Viral Analyzer

**AI-powered web app to predict and improve YouTube video virality.**  
Built with Streamlit + OpenAI + PIL.  
Created by [@valm10](https://github.com/valm10)

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?style=flat)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/UI-Streamlit-ff4b4b)](https://streamlit.io/)
[![OpenAI GPT-4](https://img.shields.io/badge/Model-GPT--4o-success)](https://openai.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

---

## 🔍 What It Does

- 📌 Upload your **YouTube title** and **thumbnail**
- 🧠 Uses **GPT-4o** to:
  - Rewrite your title to boost virality
  - Suggest thumbnail design improvements
- 📈 Gives a **mock virality score** + trending video examples
- 💡 Falls back to predictions when no API key is found

---

## ⚙️ How It Works

ViralCheck combines:

- 🖼️ Aspect ratio check for thumbnail validation (16:9 recommended)
- 🧠 GPT-4o prompt: builds a context aware query to improve title/thumbnail
- 🔄 Fallback logic: if no API key or error, shows high-quality mock predictions

All business logic is modular, testable, and logged.

---

## 🚀 Try It Locally

```bash
git clone https://github.com/valm10/viralcheck.git
cd viralcheck
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to the .env file
streamlit run app.py
