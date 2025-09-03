from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class JiraTicketRequest(BaseModel):
    summary: str
    description: str
