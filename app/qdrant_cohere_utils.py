import os
import cohere
from qdrant_client import QdrantClient
from qdrant_client import models
from qdrant_client.http import models as rest

# load environment variables
QDRANT_HOST = os.environ.get("QDRANT_HOST")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

vector_size = 768
MLLM_MODEL = "multilingual-22-12"

cohere_client = cohere.Client(COHERE_API_KEY)

qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    prefer_grpc=True,
    api_key=QDRANT_API_KEY,
)


def get_qdrant_collection_name(user_input: str):
    if user_input == "terms of service":
        collection_name = "legal_qa"
    elif user_input == "caselaw":
        collection_name = "caselaws"
    elif user_input == "legislation":
        collection_name = "legislations"
    elif user_input == "contracts":
        collection_name = "multilingual_legal_contracts"
    return collection_name


def get_embedding_size(model_name: str):
    if model_name == "large":
        embedding_size = 4096
    elif model_name == MLLM_MODEL:
        embedding_size = 768
    return embedding_size


def create_qdrant_collection(vector_size):
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size, distance=rest.Distance.DOT
        ),
    )


def embed_legal_docs(cohere_client, legal_docs):
    legal_docs_embeds = cohere_client.embed(
        texts=legal_docs,
        model="multilingual-22-12",
    )
    doc_embeddings = [
        list(map(float, vector)) for vector in legal_docs_embeds.embeddings
    ]
    doc_ids = [id for id, entry in enumerate(legal_docs_embeds)]
    return doc_embeddings, doc_ids


def embed_user_query(user_query):
    embeddings = cohere_client.embed(
        texts=[user_query],
        model=MLLM_MODEL,
    )
    return embeddings


def upsert_data_in_collection(qdrant_client, vectors, ids, payload):
    qdrant_client.upsert(
        collection_name=collection_name,
        points=rest.Batch(
            ids=ids,
            vectors=vectors,
            payloads=payload,
        ),
    )


def search_docs_for_query(
    qdrant_client,
    query_embedding,
    num_results,
    user_query,
    languages,
    doc_type,
    match_language,
):
    filters = []
    collection_name = "covid19"

    language_mapping = {
        "Dutch": "nl",
        "English": "en",
        "French": "fr",
        "Hungarian": "hu",
        "Italian": "it",
        "Norwegian": "nb",
        "Polish": "pl",
    }

    if match_language:
        filters.append(
            models.FieldCondition(
                key="text",
                match=models.MatchText(text=user_query),
            )
        )

    # if match_language:
    if languages:
        for lang in languages:
            filters.append(
                models.FieldCondition(
                    key="language",
                    match=models.MatchValue(
                        value=language_mapping[lang],
                    ),
                )
            )
    
    result = qdrant_client.search(
        collection_name=collection_name,
        query_filter=models.Filter(should=filters),
        search_params=models.SearchParams(hnsw_ef=128, exact=False),
        query_vector=query_embedding,
        limit=num_results,
    )
    return result


def translate_output(input_sentence, user_query):
    response = cohere_client.tokenize(text=input_sentence)
    
    src_detected_lang = cohere_client.detect_language(texts=[input_sentence])
    src_current_lang = src_detected_lang.results[0].language_name
    print("src_current_lang:", src_current_lang)
    
    target_detected_lang = cohere_client.detect_language(texts=[user_query])
    target_current_lang = target_detected_lang.results[0].language_name
    
    # target_current_lang = "English"
    # if src_current_lang == "English":
    #     return input_sentence
    
    prompt = f""""
    Translate this sentence from {src_detected_lang} to {target_current_lang}: '{input_sentence}'.
    
    Don't include the above prompt in the final translation. The final output should only include the translation of the input sentence.
    """

    response = cohere_client.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=len(response.tokens) * 3,
        temperature=0.6,
        stop_sequences=["--"],
    )

    translation = response.generations[0].text
    print("translation:",translation)
    return translation


def cross_lingual_document_search(
    user_input: str, num_results: int, languages, doc_type, text_match
):
    query_embed = embed_user_query(user_input)
    query_embedding = query_embed.embeddings[0]

    result = search_docs_for_query(
        qdrant_client,
        query_embedding,
        num_results,
        user_input,
        languages,
        doc_type,
        text_match,
    )
    final_results = [result[i].payload["text"] for i in range(len(result))]

    if num_results > len(final_results):
        remaining_inputs = num_results - len(final_results)
        for i in range(remaining_inputs):
            final_results.append("")

    return final_results
