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

flowchart TD
    A["🌐 Frontend React App<br/>localhost:3000"] -->|User Input| B["Chat Interface<br/>App.js"]
    B -->|User Query + Optional PDF| C["Send Message Handler"]
    C -->|FormData| D["POST /upload Endpoint"]
    C -->|Query String| E["POST /query Endpoint"]
    
    D -->|File Upload| F["Save PDF to<br/>uploaded_pdfs/"]
    F -->|File Path| G["query_agent<br/>edy_agent.py"]
    
    E -->|Query| G
    
    G -->|Load or Create| H["build_faiss_index<br/>embedding_tool.py"]
    H -->|Extract Text| I["extract_pdf_chunks<br/>pdf_tool.py"]
    I -->|Text Chunks<br/>50 chars limit| J["List of Chunks<br/>{text, source, page}"]
    J -->|Texts| K["Encode with<br/>Sentence Transformer"]
    K -->|Embeddings| L["Create FAISS Index<br/>IndexFlatL2<br/>L2 Distance"]
    L -->|Save| M["INDEX_PATH &<br/>CHUNK_PATH"]
    
    L -->|Index| N["Retrieve Top 10<br/>Similar Chunks"]
    M -->|Load| N
    
    N -->|Query Embedding| O["FAISS Search<br/>np.array query"]
    O -->|10 Chunks| P["relevant_chunks"]
    
    P -->|Chunks + Query| Q["is_query_relevant<br/>relevance_tool.py"]
    Q -->|GPT-4o-mini<br/>Classifier| R{Is Escalation<br/>Needed?}
    
    R -->|Yes| S["create_jira_ticket<br/>jira_tool.py"]
    S -->|Ticket ID| T["update_jira_ticket<br/>Add Extra Fields"]
    T -->|Return| U["Return Escalation<br/>Message to User"]
    
    R -->|No| V["Build Context Prompt<br/>From Chunks"]
    V -->|Context + Query| W["GPT-4 Chat Completion"]
    W -->|Model: gpt-4<br/>Temp: 0.2<br/>Max 30 words| X["Generate Answer"]
    X -->|Answer String| Y["Return Response<br/>to Frontend"]
    
    U -->|Bot Message| Z["Display in Chat<br/>with Markdown Links"]
    Y -->|Bot Message| Z
    Z -->|Render| A
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style L fill:#e8f5e9
    style Q fill:#fce4ec
    style W fill:#f3e5f5
    style Z fill:#fff3e0

