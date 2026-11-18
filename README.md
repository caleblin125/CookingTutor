# CookingTutor

An AI recipe tutor built with **Streamlit** and **Google Gemini**. Ask a cooking
question, optionally upload photos of your ingredients or dish, and the tutor
answers with a full recipe (ingredients, steps, timing, and dietary
substitutions) grounded in live web search results and with sources cited.

Built as the final project for the GenAI Tutor Bootcamp (2025) with
[@evelyntseng99](https://github.com/evelyntseng99).

## How it works

1. **Multimodal input:** the user types a question and can upload images
   (`.jpg`, `.png`, `.webp`).
2. **Search grounding:** if images are attached, Gemini first describes them in
   a few words; that description plus the question is sent to Google Search
   through [SerpAPI](https://serpapi.com/), and the top three results (snippet +
   link) are collected.
3. **Answer generation:** Gemini 2.0 Flash receives a tutor system prompt, the
   user's question, the search snippets, and the images, and writes a recipe
   that cites its sources.
4. Each exchange is appended to `static/log.txt`, which is shown as the
   conversation history.

[`RAG_simple.ipynb`](RAG_simple.ipynb) is the notebook prototype of the
retrieval-augmented generation pipeline, and
[`Final Presentation.pdf`](Final%20Presentation.pdf) is the project
presentation.

## Setup

```bash
pip install streamlit google-generativeai google-genai google-search-results pillow
```

Create two files containing your API keys (both are git-ignored):

```
static/key.txt         # Google Gemini API key
static/searchkey.txt   # SerpAPI key
```

Then run:

```bash
streamlit run CookingTutor.py
```

For the notebook, set the `GOOGLE_API_KEY` environment variable instead.
