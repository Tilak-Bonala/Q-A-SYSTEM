## 1. Design Notes

#### Tavale planner chat boat

Buil Chat system that can answer your NLP questions using a dataset contains member messages.

#### Apporch
 Using string matches to find relevant messages converting them into embeddings using huggingface then storing them in Pineconve vector database, and use sementic similarity for retrieval.

 Fine tuninng a LLM grok model directly on dataset to answer questions and then prompt a large language with all available data.

## 2. Data Insights

- **Source:** TravelPlanner/member messages (osunlp/TravelPlanner on HuggingFace).
- **Data Structure:** Multiple splits (train, test, validation), each with columns: member_id, message, timestamp, etc.

### Anomalies and Inconsistencies
The data looks identical or nearly identical messages repeatedly.
In the `train` split, there are periods with a high density of messages, followed by gaps, which could affect time-based analytics.
CSV files contain non-UTF-8 encoded characters, which caused UnicodeDecodeErrors during loading .
A few rows are missing member IDs or message text; these rows were dropped for processing.
Distribution is highly skewed — some messages are 1-2 words, others are long paragraphs.
Overlap in message topics between train and test sets could cause information leakage if not carefully split.


### Actions Taken

- Dropped empty or invalid rows during preprocessing.
- Applied encoding fix (`utf-8`) for robust CSV parsing.
- Noted duplicates and highly similar entries, but retained them to avoid losing genuine repeated queries.

# How to run?
### STEPS:

Clone the repository

```bash
Clone the repository

```
### STEP 01- Create a conda environment after opening the repository

```bash
 conda create -n medibot python=3.10 -y
```

```bash
 conda activate medibot
```

### STEP 02- install the requirements
```bash

pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Pinecone & openai credentials as follows:

```ini
 PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 GROQ_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
## run the following command to store embeddings to pinecone
python store_index.py
```

```bash
## Finally run the following command
python app.py
```

Now,
```bash
open up localhost: http://localhost:8080/apidocs
```


### Techstack Used:

- Python
- LangChain
- Flask
- Groq
- Pinecone