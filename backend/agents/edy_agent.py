from config import OPENAI_CLIENT, MODEL
from tools.embedding_tool import build_faiss_index
from tools.relevance_tool import is_query_relevant
from tools.jira_tool import create_jira_ticket, update_jira_ticket


import numpy as np

# Load index on startup
faiss_data = build_faiss_index()
INDEX = faiss_data["index"]
CHUNKS = faiss_data["chunks"]

def query_agent(query: str,pdf_filename: str = None) -> str:
    """
    Main agent function:
    1. Retrieves top chunks using FAISS
    2. Checks relevance
    3. Escalates via Jira if needed
    4. Answers using OpenAI
    """
    query_embedding = MODEL.encode([query])
    D, I = INDEX.search(np.array(query_embedding), 10)
    relevant_chunks = [CHUNKS[i] for i in I[0]]
    top_score = D[0][0]
    context_prompt= """You are an AI assistant named Edy, and you are tasked with answering EdMyst related 
  queries asked by users curious about EdMyst services. You have access to a large database containing information
  about EdMyst Operations and Offerings. Please make sure your responses are aligned with that of a customer representative.
  Please make sure your responses are of 30 words or less. Please also ensure that you ONLY answer what the user asks.
  Below is the user query. If you include any links, format them as proper Markdown hyperlinks: [text](https://example.com) 
The user will see clickable links. Here are the links :\n
"https://www.edmyst.coach" ,  "https://www.edmyst.coach/calculator", "https://www.edmyst.com",
 Do NOT tell the user that there is a text provided to you, and Respond nicely if the user has a generic greeting or a thank you in their message politely.
 If the user is talking about something irrelevant, please say "I am only trained to answer questions about EdMyst. If you have a question about EdMyst, please ask it directly."
 DO NOT talk about context. Your answer is directly forwarded to the user. now, here is the user query: \n """
    # Escalate if no relevant info
    print("relevant scores:", top_score)
    if not relevant_chunks or top_score > 1.0:
        if is_query_relevant(query, relevant_chunks):
            
            ticket_id = create_jira_ticket(
                summary="Chatbot Escalation Request",
                description=f"User query: {query}",
                pdf_filename=pdf_filename
            )

            extra_fields = {
                "assignee": {"id": "USER_ACCOUNT_ID"},   # or {"accountId": "..."} depending on API
                "duedate": "2025-09-01",
                 "customfield_12345": "High"              # e.g. priority, start date, etc.
            }

            update_jira_ticket(ticket_id, extra_fields)

            return f"I couldn't find the answer right now, so I've forwarded your question to our team. They will get back to you soon."
        
    # Build context for OpenAI
    context = "\n\n".join(f"[{c['source']} p{c['page']}]: {c['text']}" for c in relevant_chunks)
   

    prompt = f"""Use the context below to answer the question. keep the context in mind.

            Context:
            {context}
            {context_prompt}

            Question: {query}"""


    response = OPENAI_CLIENT.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


#712020:3fd7ee25-1617-4ee7-8409-3d45398c0e22