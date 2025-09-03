import requests, os
from dotenv import load_dotenv
load_dotenv()

from config import UPLOAD_DIR

def create_jira_ticket(summary: str, description: str, pdf_filename: str = None) -> str:
    """
    Creates a Jira ticket and returns ticket ID.
    """
    url = f"https://{os.getenv('JIRA_DOMAIN')}/rest/api/3/issue"
    auth = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    
    adf_description = {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
    }

    payload = {
        "fields": {
            "project": {"key": os.getenv("JIRA_PROJECT_KEY")},
            "summary": summary,
            "description": adf_description,
            "issuetype": {"id": os.getenv("JIRA_ISSUE_TYPE")}
        }
    }


    response = requests.post(url, json=payload, headers=headers, auth=auth)         
    if response.status_code not in (200, 201):
        raise Exception(f"Jira API error: {response.text}")
    
    issue_key = response.json().get("key", "unknown")
    if pdf_filename:
        pdf_path = os.path.join("uploaded_pdfs", pdf_filename)
        if os.path.exists(pdf_path):
            attach_url = f"https://{os.getenv('JIRA_DOMAIN')}/rest/api/3/issue/{issue_key}/attachments"
            attach_headers = {"X-Atlassian-Token": "no-check"}
            with open(pdf_path, "rb") as f:
                files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
                attach_resp = requests.post(attach_url, headers=attach_headers, auth=auth, files=files)
               
                if attach_resp.status_code not in (200, 201):
                    raise Exception(f"Failed to attach PDF: {attach_resp.text}")

    return issue_key
    




# Usage:


# important = filter_jira_fields(
#     fields,
#     keywords=["assignee", "start date", "description"]
# )

# for f in important:
#     print(f"{f['id']} -> {f['name']}")


def update_jira_ticket(issue_key: str, fields: dict):
    url = f"https://{os.getenv('JIRA_DOMAIN')}/rest/api/3/issue/{issue_key}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))

    payload = {"fields": fields}

    response = requests.put(url, json=payload, headers=headers, auth=auth)

    if response.status_code != 204:
        print("Failed to update ticket:", response.status_code, response.text)
    else:
        print(f"✅ Ticket {issue_key} updated successfully")
