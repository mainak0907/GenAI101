from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes # used for making fast_api out of the model
from langchain_fireworks import ChatFireworks
import uvicorn
import getpass
import os

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("FIREWORKS_API_KEY"):
  os.environ["FIREWORKS_API_KEY"] = getpass.getpass("Enter API key for Fireworks AI: ")

app=FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"

)

add_routes(
    app,
    ChatFireworks(),
    path="/llama"
)
model1=ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")

model2=ChatFireworks(model="accounts/fireworks/models/llama-v3p1-405b-instruct")

prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")

add_routes(
    app,
    prompt1|model1,
    path="/essay"


)

add_routes(
    app,
    prompt2|model2,
    path="/poem"


)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
