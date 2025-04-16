import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain_groq import ChatGroq
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(api_key=groq_api_key, model_name="mistral-saba-24b")

# 1️⃣ --- Custom Tool Class ---
class SearchSummarizerTool(BaseTool):
    name:str= "web_search_summarizer"
    description:str= "Searches the web for a query, summarizes top articles, and returns a final answer with sources."

    def _run(self, query: str):
        try:
            # Step 1: Google search
            urls = [url for url in search(query, num_results=3)]

            # Step 2: Scrape + summarize each URL
            summaries = []
            for url in urls:
                try:
                    res = requests.get(url, timeout=10)
                    soup = BeautifulSoup(res.content, 'html.parser')
                    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
                    full_text = "\n".join(paragraphs)[:3000]

                    # Summarize each page using Groq LLM
                    summary_prompt = f"Summarize the following article content:\n\n{full_text}"
                    summary = llm.invoke(summary_prompt).content.strip()

                    summaries.append({"url": url, "summary": summary})
                except Exception as e:
                    summaries.append({"url": url, "summary": f"Error summarizing {url}: {e}"})

            # Step 3: Final answer generation
            combined = "\n\n".join([f"Source: {s['url']}\n{s['summary']}" for s in summaries])
            # Add fallback guidance in case content is weak
            final_prompt = f"""
            You are an intelligent assistant helping summarize search results.

            Your job is to:
            - Extract relevant points from the article summaries that directly answer the user's question.
            - Format the answer as clear and concise bullet points.
            - If the summaries do not contain enough relevant information, say:
            "Insufficient Info. Please refer to the provided sources for more information."

            --- Article Summaries ---
            {combined}

            --- User Question ---
            {query}

            --- Your Response (in bullet points or fallback message) ---
            """
            final_answer = llm.invoke(final_prompt).content.strip()

            # Step 4: Format answer with sources
            return {
                "answer": final_answer,
                "sources": [s["url"] for s in summaries]
            }

        except Exception as e:
            return f"Tool failed: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported")

# 2️⃣ --- Load the tool and initialize the agent ---
tool_instance = SearchSummarizerTool()
tools = [tool_instance]

agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=False)

# 3️⃣ --- Streamlit UI ---
st.set_page_config(page_title="Smart Web Agent", layout="centered")
st.title("🤖 Smart Web Answer Agent 🤖")
st.caption("Ask anything. It will search, summarize, and answer with source links.")

query = st.text_input("👇 Enter your question", placeholder="Type and hit Enter...")

if query:  # This will trigger when user presses Enter
    with st.spinner("🔍 Searching and summarizing..."):
        tool_instance = SearchSummarizerTool()
        result = tool_instance._run(query)

    st.markdown(f"### ✅ Answer\n{result['answer']}")
    st.markdown("### 🔗 Sources")
    for i, url in enumerate(result["sources"], start=1):
        st.markdown(f"{i}. [{url}]({url})")