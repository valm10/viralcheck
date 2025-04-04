# 📈 ViralCheck – YouTube Viral Analyzer

Boost your YouTube video's chance of success with AI.  
🎯 Predict virality, improve titles, and thumbnail tips.

![Demo](assets/demo.gif)

---

### 🧠 Features

- ✅ Upload a video **title** and **thumbnail**
- 🤖 Get an **AI-suggested improved title**
- 💡 Receive **title and thumbnail tips**
- 🔍 View **real YouTube videos** similar to your title
- 💥 Mock fallback logic if GPT is unavailable

---

### 🛠️ Tech Stack

| Tool           | Purpose                             |
|----------------|-------------------------------------|
| `Streamlit`    | Frontend UI                         |
| `OpenAI GPT-4o`| Title + Thumbnail suggestion engine |
| `yt-dlp`       | Real YouTube search results         |
| `Pillow`       | Image ratio validation              |
| `dotenv`       | API key management                  |
| `Python`       | Everything glued together           |

---

## 📦 Installation

```bash
git clone https://github.com/valm10/viralcheck.git
cd viralcheck
python3 -m venv venv
source venv/bin/activate # or .\\venv\\Scripts\\activate on Windows
pip install -r requirements.txt
#Create .env file and Paste OPENAI_API_KEY=your-key-here
streamlit run app.py

