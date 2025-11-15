from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from dotenv import load_dotenv
from src.helper import download_embeddings
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt
import os

app = Flask(__name__)
swagger = Swagger(app)
load_dotenv()

# Load API keys
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Load embeddings
embeddings = download_embeddings()

# Connect to Pinecone vector index
index_name = "qa-system"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Build RAG retriever + LLM model
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

chat_model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

qa_chain = create_stuff_documents_chain(chat_model, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

# -------------------------
#   MAIN API ENDPOINT
# -------------------------

@app.route("/ask", methods=["POST"])
@swag_from({
    'tags': ['TravelPlanner'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'question': {
                        'type': 'string',
                        'example': '"What attractions do you recommend in Rockford?'
                    }
                },
                'required': ['question']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Answer to the travel question',
            'schema': {
                'type': 'object',
                'properties': {
                    'answer': {
                        'type': 'string',
                        'example': 'My plan recommends visiting the Klehm Arboretum & Botanic Garden and Sinnissippi Park in Rockford as attractions.'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        500: {
            'description': 'Server error'
        }
    }
})

def ask_question():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if question.strip() == "":
            return jsonify({"error": "Question cannot be empty"}), 400

        response = rag_chain.invoke({"input": question})
        return jsonify({"answer": response["answer"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "TravelPlanner API running", "usage": "POST to /ask with {question}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
