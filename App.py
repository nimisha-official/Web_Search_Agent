import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain_groq import ChatGroq
from googlesearch import search
from bs4 import BeautifulSoup
import requests