import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")
BITBUCKET_API_TOKEN = os.getenv("BITBUCKET_API_TOKEN")
ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN")


def comment_on_pr_from_bitbucket(pr_id, file_path, comments):
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests/{pr_id}/comments"
    payload = {"content": {"raw": f"{comments}"}, "inline": {"path": file_path, "to": 1}}
    response = requests.post(url, json=payload, headers={
        "Authorization": f"Bearer {BITBUCKET_API_TOKEN}",
        "Content-Type": "application/json",
    })
    response.raise_for_status()
    return response


def get_content_on_pr_from_bitbucket(pr_id):
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests/{pr_id}"
    response = requests.get(url, headers={
        "Authorization": f"Bearer {BITBUCKET_API_TOKEN}",
        "Content-Type": "application/json",
    })
    response.raise_for_status()
    result = response.json()
    return result


def get_issue_from_jira(issue_id):
    url = f"https://smarterweb.atlassian.net/rest/api/3/issue/{issue_id}"
    response = requests.get(url, headers={"Accept": "application/json"}, auth=HTTPBasicAuth("lucio.gerardo@sw.com.mx", ATLASSIAN_API_TOKEN))
    response.raise_for_status()
    result = response.json()
    text = ""
    for description in result["fields"]["description"]["content"]:
        content = description["content"][0]
        if content["type"] == "text":
            text += content["text"] + "\n"

    title = result["fields"]["summary"]
    return title, text
