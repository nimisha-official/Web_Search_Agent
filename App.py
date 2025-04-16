import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain_groq import ChatGroq
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

# Load secret values from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=groq_api_key, model_name="mixtral-8x7b-32768")

# 1️⃣ --- Custom Tool Class ---
class SearchSummarizerTool(BaseTool):
    name = "web_search_summarizer"
    description = "Searches the web for a query, summarizes top articles, and returns a final answer with sources."

    def _run(self, query: str):
        try:
            # Step 1: Google search
            urls = [url for url in search(query, num_results=5)]

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
            final_prompt = f"Using the following summaries, answer the question:\n\n{combined}\n\nQuestion: {query}"
            final_answer = llm.invoke(final_prompt).content.strip()

            # Step 4: Format answer with sources
            formatted = f"**Answer:**\n{final_answer}\n\n**Sources:**\n"
            for s in summaries:
                formatted += f"- {s['url']}\n"
            return formatted

        except Exception as e:
            return f"Tool failed: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported")

# 2️⃣ --- Load the tool and initialize the agent ---
tool_instance = SearchSummarizerTool()
tools = [tool_instance]

