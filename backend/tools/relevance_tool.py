from config import OPENAI_CLIENT
import json
def is_query_relevant(query: str, chunks: list) -> bool:
    """
    Determines if a user query is relevant to EdMyst knowledge base.
    Returns True if escalation is needed.
    """
    prompt = f"""
 You are a classifier.  Determine if the following user query is relevant to Edmyst, the online learning and mentorship platform.
 Ignore any unnnecessary information or words in the query .
    If the query is a greeting or a conversational piece, say "no".If the query is a vague question about some company, say "no".
    If the query is about EdMyst and the retrieved chunks can answer it, reply with "no". If the user is asking for a link, say "no".
    If the query is irrelevant to EdMyst, reply with "yes". 
      If the query is a question about EdMyst that the retrieved chunks
    cannot answer,reply with "yes". \n
    Reply only with "yes" or "no".\n
    Chunks: {json.dumps(chunks, indent=2)}\n
    Query: {query}
    
    """
    
    response = OPENAI_CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    print(response.choices[0].message.content.strip().lower())
    return response.choices[0].message.content.strip().lower().startswith("y")
