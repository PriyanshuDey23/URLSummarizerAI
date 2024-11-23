from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *
from bs4 import BeautifulSoup
import requests

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



# Function to extract text from URL
def extract_text_from_url(url):
    response = requests.get(url)
    response.status_code == 200
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract readable text, here filtering out JavaScript, CSS, and other unwanted tags
    text = ' '.join([p.get_text() for p in soup.find_all("p")])
    return text
    


# Response Format For my LLM Model
def Summarization_chain(input_text, tone, word_count):
    # Define the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002", temperature=1, api_key=GOOGLE_API_KEY)  
    
    # Define the prompt
    PROMPT_TEMPLATE = PROMPT  # Imported
    prompt = PromptTemplate(
            input_variables=["text", "tone", "word_count"], # input in prompt
            template=PROMPT_TEMPLATE,
        )
      
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate response
    response = llm_chain.run({"text": input_text, "tone": tone, "word_count": word_count})
    return response


# Streamlit app
st.set_page_config(page_title="URL Summarizer")
st.header("URL Summarizer")

# URL input
url = st.text_input("Enter a URL")

# Parameters
column_1, column_2 = st.columns([5, 5])

# Tone selection
with column_1:
    tone = st.selectbox("Select the tone", ["Formal", "Informal", "Friendly", "Professional"])

# Word count selection
with column_2:
    word_count = st.text_input("Number Of Words")

# Summarize button
if st.button("Summarize") and url:
    if word_count.isdigit():
        # Extract text from URL
        url_text = extract_text_from_url(url)
        
        # Ensure there's content to summarize
        response = Summarization_chain(input_text=url_text, tone=tone, word_count=int(word_count))
            
        # Display the results
        st.write(" The Summary is: \n \n" ,response )

