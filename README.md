# [Project Submission for Multilingual Semantic Search Hackathon](https://lablab.ai/event/multilingual-semantic-search-hackathon)

## Legal-ease : Your Legal AI Copilot

<p align="center">
  <img src="logo/flc_design4.png" alt="Legal-ease Logo" />
</p>

We've made tremendous advancements in the domain of natural language processing recently. The language models available today are capable of doing everything from text generation to question answering and what not. 

We feel a great application of this technology can be in the legal domain which is filled with giant corpuses of text which are generally too complex for a person to understand especially without any expertise or knowledge about the domain itself. And this is one of the main reasons that inspired us to create **Legal-ease**.

Simply put, Legal-ease is a web-app to simplify working with legal documents.

## Problem with Legal Data
You might be wondering, why would we need a dedicated tool for handling legal data when a lot of general purpose document tools are available. Well that's because legal data comes with its own set of niche problems. Here are a few of them:
- Legal documents come in all shapes and sizes i.e. contracts, patents, licenses, etc.
- They are usually lengthy and pretty dense to comprehend for a layman.
- More often then not, these documents are found in languages other than English.
- These documents are often written with complex sentence structure and grammar which is not found in general spoken/written language.

## What's the solution?
We aim to solve the issues and difficulties faced in understanding legal documents via a bunch of features:

<p align="center">
  <img src="logo/legal-ease.png" alt="Legal-ease app" />
</p>
    
1. **QnA over legal documents**: With the help of this feature, we enable a user to ask any questions and clarify doubts that they may have regarding a particular legal document. 
2. **Legal Document summarization**: As mentioned earlier, legal documents can be very lengthy and most of the times, we just need a quick summary to get going. With this feature a user can generate "small*", "medium" or "long" summaries for legal documents in the form of "paragraphs" or "bullet points". 
3. **Multi & Cross-lingual document search**: With this feature, a user can search across huge piles of documents to retrieve some document they may require. Both multi-lingual and cross-lingual searching capabilities are supported as part of this feature. 

We feel the Q&A and summarization feature can be useful for both layman and experts of legal domain. Although it certainly been designed with the intent of making the process of comprehending legal docs simpler for a layman.

The document search feature is targeted more towards people working actively with legal documents such as lawyers, judges, researchers, law students, policy makers, etc who may benefit from being able to search through giant list of text heavy documents within seconds to find what they may be looking for almost instantly.
A layman who has a good chunk of legal documents to keep track of can also benefit from such a feature. 

Overall we feel, this solution can be beneficial for both layman and legal experts.

    
## Tools & Technologies Used:
 1. [**Cohere**](https://docs.cohere.ai/docs/the-cohere-platform): Cohere offers capability to add cutting-edge language processing to any system. They train massive language models which accessible via simple APIs. We have used the following APIs offered by Cohere for a bunch of different tasks:
     - Retrieving embeddings for a given input document which can be inserted into Qdrant DB and utilized to support document search feature using [co.embed](https://docs.cohere.ai/reference/embed)
     - Generating summaries using [co.summarize](https://docs.cohere.ai/reference/summarize-2)
     - Generating answers for the question based on the given document by the user using [co.generate](https://docs.cohere.ai/reference/generate)
     - Generating translation for a given input using [co.generate](https://docs.cohere.ai/reference/generate)
     - Performing language detection on input queries as part of document search module using [co.detect_language](https://docs.cohere.ai/reference/detect-language-1)
     - Tokenizing an input sentence using [co.tokenize](https://docs.cohere.ai/reference/tokenize)
     
We've used Cohere's `multilingual-22-12` model for retrieving multilingual embeddings to support multi-lingual semantic search, `summarize-xlarge` model for summarization task and `command-xlarge-nightly` for performing text generation tasks such generating answers or translation for an input query.
         
 2. **[Qdrant]((https://qdrant.tech/))**: It is a vector similarity engine & vector database. It deploys as an API service providing search for the nearest high-dimensional vectors. We have used Qdrant to implement the following features:
     - **Document Search**: Qdrant is built using Rust which makes it extremely fast and can be used to perform and retrieve search across giant collections of embeddings and get results almost instantaneously. In the interest of time, we have already taken a [sample dataset](https://huggingface.co/datasets/joelito/covid19_emergency_event) and added its embeddings to a Qdrant [**collection**](https://qdrant.tech/documentation/collections/). Our search module supports the following features:
         - **Semantic search**: A user can input a query and Qdrant will use the query embeddings and compare it against the available embeddings its database using a distance metric called "DOT" product to return the most similar embeddings. Since we are using Cohere's `multilingual-22-12` model for creating embeddings we must use dot product as the distance metric because the model was trained using dot product calculations.
         - **Payloads for better search**: Using qdrant it was very easy to create a collection and add payloads (additional metadata) for collections.
         - **Filters for search**: We also leveraged filters feature of qdrant to search relevant documents based on the information available in the payloads. For instance, we added filters for filtering documents on basis of language/country of origin of the documents as part of our example search use case.
         - **Search is multilingual**: Since we have used multlingual embeddings using cohere, the user can input a search query in a language of their choice and get documents that may not be in the same language as the query entered by the user but contain the same context as conveyed by the user's query. 
         - **Hybrid Search**: It's beneficial sometimes to have the capability to do both keyword and semantic search. With Qdrant it's very easy to look for exact phrases or words using their full-text-match filter and also have the results ranked by a similarity score. Thus supporting a dual search option if the user requires it. 
    
    - **Question Answering**: Qdrant's semantic search capability has also been used as part of our Q&A module. Qdrant is used to find the most relevant portion of the document that may be similar to the question that has been asked by the user. A text generation model is then used to generate the final answer using question and relevant context identified via qdrant as input. Although in this case, we haven't used the qdrant-client directly but instead made use of Langchain wrappers for Qdrant.


     
 3. **[Langchain](https://langchain.readthedocs.io/en/latest/getting_started/getting_started.html)**: It is an open source library that provides abstractions for building LLM-based applications. Langchain makes it easy and fast to put together an end-to-end application via its wide range of modules. 
 In our case, we have leveraged langchain's wrappers for cohere and qdrant to support the Q&A usecase.
 4. **[Gradio](https://gradio.app/docs/)**: The frontend of the application is built using Gradio. We've used a bunch of features like:
     - Blocks API for overall app design.
     - Leveraged components like Chatbot, TextBox, Checkboxgroup, Accordion, Button , etc.
     - And utilized its support for event listening to build features like "search as you type" and Q&A , etc 
 
 5. [**HF Spaces**](https://huggingface.co/docs/hub/spaces-overview): Hugging Face Spaces offer easy and affordable deployment support for ML applications. We have leveraged the same for our app. Here's the [link to our Space.](https://huggingface.co/spaces/Legal-ease/legal-ease).

## Installation: Try it out!

1. Make sure you have a cohere account and you've set the COHERE_API_KEY environment variable.
2. Create a free-tier Qdrant cluster and set the following environment variables - QDRANT_API_KEY AND QDRANT_HOST. You can also setup Qdrant locally using docker or helm if you prefer. Here are the [instructions](https://qdrant.tech/documentation/install/).
3. Install requirements.
    ```shell
        cd <project_dir>`
        conda create -n legal-ease --file requirements.txt
        conda activate legal-ease
    ```
4. To run the app locally, use the following command:
    ```shell
    python gradio_demo.py
    ```
    If you want to run the app in reload mode then run:
    ```shell
    gradio gradio_demo.py
    ```
    The app should typically appear on the url: `http://localhost:7860`

Note: For the document search feature to work, you would need a giant corpus


## References:
- [Langchain Question-Answering guide](https://langchain.readthedocs.io/en/latest/use_cases/question_answering.html)
- [MultiLingual Semantic Search using Cohere and Langchain](https://txt.cohere.ai/search-cohere-langchain/)
- [Q&A with Cohere and Qdrant](https://qdrant.tech/articles/qa-with-cohere-and-qdrant/)
- [Semantic Search Livestream with Cohere and Qdrant team organized by LabLab.ai](https://www.twitch.tv/videos/1764056911) 

## Acknowledgements:
- We'd like to thank [Joel Niklaus](https://huggingface.co/joelito) for open-sourcing so many datasets and models related to the legal domain. We particularly found the [english_contracts_summarization](https://huggingface.co/datasets/joelito/plain_english_contracts_summarization) and [covid19_emergency_event](https://huggingface.co/datasets/joelito/covid19_emergency_event) datasets to be very useful for our project. We'd definitely recommend anyone working in the legal AI domain to check out his work.

