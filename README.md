__Description__

This AI Assistant utilizes a simple chunking function `(extract_pdf_chunks)`that splits PDF page text into chunks based on a character count limit `(chunk_size)`. Then, it builds a FAISS (Facebook AI Similarity Search) Index in `build_faiss_index`, that utilizes a Sentence Transformer to change those chunks into vectors / word-embeddings where each embedding is a fixed-length float vector (384 dimensions here).
`IndexFlatL2` creates a flat (brute-force) index that stores all vectors in memory, using L2 distance (Euclidean distance) as the similarity metric.
To find chunks similar to a query, and to feed them to the AI Assistant, we convert the query into a similar vector, and use the top 10 results as context for the AI Assistant to formulate its answer. 
The `relevance_tool` is another screening, whereby first, we check if the query and resulting chunks can actually answer the query, or if they are relevant to EdMyst. Accordingly, either the AI Assistant returns its response, or a JIRA ticket is raised for the same.


__Instructions to set up AI Assistant__


To run this AI Assistant, you need some things set up :

In the `backend` :
* create a virtual environment in Python
* download all the packages needed in the `requirements.txt` file.
* ensure you have the necessary keys and tokens listed in the `.env` file.
* Add your database as pdf files in the folder `data`. Everytime you add files, and rerun the chatbot, make sure you delete the word-embedding chunks and index files from `storage`. The AI Assistant only recreates these files when they don't exist.
* run `uvicorn main:app --reload --host 0.0.0.0 --port 8000` inside the virtual environment.
  
In the `frontend` :
* You need to have Create React App installed for the frontend to configure properly; refer to the `package.json` file.
* run `npm start`, and click on the link that appears for your local run of the AI Assistant.



