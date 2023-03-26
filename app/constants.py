# name of cohere's summarization model
SUMMARIZATION_MODEL = "summarize-xlarge"

# path of the csv file containing the example legal documents
EXAMPLES_FILE_PATH = "app/examples.csv"

# whether to use multilingual embeddings to represent the documents or not
USE_MULTILINGUAL_EMBEDDING = True

# name of cohere's multilingual embedding model
MULTILINGUAL_EMBEDDING_MODEL = "multilingual-22-12"

# name of cohere's default embedding model
ENGLISH_EMBEDDING_MODEL = "large"

# The name with which you want to create a collection in Qdrant
CREATE_QDRANT_COLLECTION_NAME = "covid19"

# name of cohere's model which will be used for generating the translation of an input document
TEXT_GENERATION_MODEL = "command-xlarge-nightly"

# whether the search results obtained via document search module should be translated into the language which was used by the user to type their `search query`.
TRANSLATE_BASED_ON_USER_QUERY = False

# If you have multiple collections inside your Qdrant DB, make sure the value of this variable is set to the name of the collection on which you want to enable search.
SEARCH_QDRANT_COLLECTION_NAME = "covid19"
