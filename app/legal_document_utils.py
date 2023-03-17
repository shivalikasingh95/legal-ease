import os, cohere
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Qdrant
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
import pandas as pd

# load environment variables
QDRANT_HOST = os.environ.get("QDRANT_HOST")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

# define constants
SUMMARIZATION_MODEL = "summarize-xlarge"


def summarize(
    document: str,
    summary_length: str,
    summary_format: str,
    extractiveness: str,
    temperature: float,
):
    
    summary_response = cohere.Client(COHERE_API_KEY).summarize(
        text=document,
        length=summary_length,
        format=summary_format,
        model=SUMMARIZATION_MODEL,
        extractiveness=extractiveness,
        temperature=temperature,
    )
    return summary_response.summary


def question_answer(input_document, history):
    context = input_document
    question = history[-1][0]

    texts = [context[k : k + 256] for k in range(0, len(context.split()), 256)]

    embeddings = CohereEmbeddings(
        model="multilingual-22-12", cohere_api_key=COHERE_API_KEY
    )
    context_index = Qdrant.from_texts(
        texts, embeddings, host=QDRANT_HOST, api_key=QDRANT_API_KEY
    )

    prompt_template = """Text: {context}

    Question: {question}

    Answer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available."""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Generate the answer given the context
    chain = load_qa_chain(
        Cohere(
            model="command-xlarge-nightly", temperature=0, cohere_api_key=COHERE_API_KEY
        ),
        chain_type="stuff",
        prompt=PROMPT,
    )
    relevant_context = context_index.similarity_search(question)
    answer = chain.run(input_documents=relevant_context, question=question)
    answer = answer.replace("\n", "").replace("Answer:", "")
    return answer

def load_gpl_license():
    df = pd.read_csv("app/examples.csv")
    return df['doc'].iloc[0], df['question'].iloc[0]

def load_pokemon_license():
    df = pd.read_csv("app/examples.csv")
    return df['doc'].iloc[1], df['question'].iloc[1]