
# 🤖 Smart Web Answer Agent

An intelligent web agent built using Streamlit, LangChain, and Groq's LLM to answer user questions using real-time web search and summarization.

---

## 🧠 How It Works

1. The user submits a natural language query.
2. The app fetches the top 3 Google search results using `googlesearch-python`.
3. Each result is scraped for paragraph content using `requests` + `BeautifulSoup`.
4. Summaries of the pages are generated using Groq's `mistral-saba-24b` model.
5. A final answer is generated in bullet points, or a fallback message is shown if no info is found.
6. The user receives a clean, concise response with source links.

---

## 🛠️ Tech Stack

| Tool/Library         | Purpose                                  |
|----------------------|-------------------------------------------|
| Streamlit            | Front-end for user interaction            |
| LangChain            | Agent and tool abstraction                |
| langchain-groq       | Integration with Groq-hosted LLMs         |
| googlesearch-python  | To fetch top Google search results        |
| BeautifulSoup        | HTML parsing                              |
| requests             | Web scraping                              |
| python-dotenv        | Managing environment variables securely   |

---

## 📸 Screenshots

![App Screenshot](https://i.imgur.com/n3QKpYh.png)

---

## 🔗 Deployed Link

👉 [Launch App on Streamlit Cloud](https://your-app-link.streamlit.app)

