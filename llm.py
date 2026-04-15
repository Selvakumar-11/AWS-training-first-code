##-----------Simple chatbot ------------------------##

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, chain
from fastapi import FastAPI , HTTPException
from dotenv import load_dotenv
load_dotenv()

import os

app = FastAPI()

##---------------- Define LLM -------------------##

headers = {
    'x-service-line': os.getenv('SERVICE_LINE'),
    'x-brand': os.getenv('BRAND'),
    'x-project': os.getenv('PROJECT'),
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'api-version': os.getenv('HEADER_API_VERSION'),
    'Ocp-Apim-Subscription-Key': os.getenv('API_KEY'),
}

llm = AzureChatOpenAI(
    model="GPT4o128k",
    api_version=os.getenv('API_VERSION'),
    azure_endpoint=os.getenv('END_POINT'),
    api_key=os.getenv('API_KEY'),
    deployment_name=os.getenv('DEPLOYMENT_ID'),
    default_headers=headers,
)

##-----------------------project_1----------------------------------------##

## defining the prompt template ##
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful ai assitant."),
    ("user","{question}")
])

chain = prompt | llm

@app.get("/get_response")
async def get_response(question: str) -> str:
    try:
        res = chain.invoke({"question": question})
        return res.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
