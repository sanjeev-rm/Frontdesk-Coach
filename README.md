# FrontDesk Coach 🛎️

FrontDesk Coach is a small training tool for hotel front-desk associates.

Instead of answering real guests, trainees type their draft reply to a **guest scenario**, and an AI “manager”:

- Scores the reply on **policy**, **tone**, and **clarity**
- Gives short, concrete feedback
- Suggests a **better wording** that keeps the same decision but uses Statler-style language

This project is for the Cornell **AI Chatbots, RAG, AI Agents** final.

---

## Tech Stack

- Python 3.12
- Streamlit (UI)
- OpenAI Agents SDK (`agents` package)
- YAML config for hotel details: `data/statler_profile.yaml`

The hotel config includes tone guidelines, key policies, and example phrases so the coach can stay specific to this property.

---

## How to Run (GitHub Codespaces)

1. **Open a Codespace** on this repo  
   Go to the repo → **Code** → **Codespaces** → **New codespace**.

2. **API key**  
   - The group OpenAI API key is stored as a **Codespaces secret** named `OPENAI_API_KEY`.
   - You do **not** need to create a `.env` file inside Codespaces.

3. **Install dependencies** (first time only):
   ```bash
   python -m pip install -r requirements.txt
4. **Run the app**:
    ```bash
   python -m streamlit run app.py