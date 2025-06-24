# 🩺 AI Health Assistant Chatbot

A multilingual AI-powered medical chatbot that provides health suggestions, symptom-based remedies, and personalized health tips. Built with `Streamlit`, `Sentence Transformers`, and `Google Translate`, it uses a CSV dataset of diseases and cures to recommend solutions or fallback suggestions in user-selected languages.

---

## 🚀 Features

- ✅ Symptom-based disease detection using sentence similarity
- ✅ Personalized health and wellness tips
- ✅ Multi-language support via `googletrans`
- ✅ Clean, responsive UI built with Streamlit
- ✅ Keyword-based fallback system for general queries

---


---

## 🛠️ Requirements

Install the following Python packages before running the app:

```bash
pip install streamlit pandas sentence-transformers googletrans==4.0.0-rc1

```
 ## 🧠 How It Works
✅ The user inputs a symptom or health-related query.
✅ The chatbot uses SentenceTransformer to encode the input and compares it with known diseases in the dataset.
✅ If similarity exceeds a threshold, it returns the most relevant cure.
✅ If no strong match is found, it uses keyword-based fallback responses (e.g., for “fever”, “cold”, “cough”).
✅ Users can also get personalized health tips based on keywords like sleep, stress, fatigue.
✅ All responses are translated into the user-selected language using Google Translate API.


🌍 Supported Languages 
The chatbot supports the following languages for input and output:
English
Hindi
Gujarati
Korean
Turkish
German
French
Arabic
Urdu
Tamil
Telugu
Chinese
Japanese

🧪 Running the App
Use the following command in your terminal
streamlit run app.py