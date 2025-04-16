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
