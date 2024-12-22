# atlassian.py
import os
import requests
from requests.auth import HTTPBasicAuth

class AtlassianConfig:
    def __init__(self):
        self.bitbucket_workspace = None
        self.bitbucket_repo_slug = None
        self.bitbucket_api_token = None
        self.atlassian_api_token = None

    def configure_bitbucket(self, workspace, repo_slug, api_token):
        self.bitbucket_workspace = workspace
        self.bitbucket_repo_slug = repo_slug
        self.bitbucket_api_token = api_token

    def configure_jira(self, api_token):
        self.atlassian_api_token = api_token
    
    def validate_bitbucket_config(self):
        if not self.bitbucket_workspace:
            raise ValueError("El workspace de Bitbucket no está configurado.")
        if not self.bitbucket_repo_slug:
            raise ValueError("El repositorio de Bitbucket no está configurado.")
        if not self.bitbucket_api_token:
            raise ValueError("El token de API de Bitbucket no está configurado.")

    def validate_jira_config(self):
        if not self.atlassian_api_token:
            raise ValueError("El token de API de Jira no está configurado.")


# Singleton instance for global configuration
config = AtlassianConfig()


def comment_on_pr_from_bitbucket(pr_id, file_path, comments, cfg=config):
    cfg.validate_bitbucket_config()
    
    url = f"https://api.bitbucket.org/2.0/repositories/{cfg.bitbucket_workspace}/{cfg.bitbucket_repo_slug}/pullrequests/{pr_id}/comments"
    payload = {"content": {"raw": f"{comments}"}, "inline": {"path": file_path, "to": 1}}
    response = requests.post(
        url,
        json=payload,
        headers={
            "Authorization": f"Bearer {cfg.bitbucket_api_token}",
            "Content-Type": "application/json",
        }
    )
    response.raise_for_status()
    return response.json()


def get_content_on_pr_from_bitbucket(pr_id, cfg=config):
    cfg.validate_bitbucket_config()
    
    url = f"https://api.bitbucket.org/2.0/repositories/{cfg.bitbucket_workspace}/{cfg.bitbucket_repo_slug}/pullrequests/{pr_id}"
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {cfg.bitbucket_api_token}",
            "Content-Type": "application/json",
        }
    )
    response.raise_for_status()
    return response.json()


def get_issue_from_jira(issue_id, cfg=config):
    cfg.validate_jira_config() 
    
    url = f"https://smarterweb.atlassian.net/rest/api/3/issue/{issue_id}"
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        auth=HTTPBasicAuth("lucio.gerardo@sw.com.mx", cfg.atlassian_api_token)
    )
    response.raise_for_status()
    result = response.json()
    text = ""
    for description in result["fields"]["description"]["content"]:
        content = description["content"][0]
        if content["type"] == "text":
            text += content["text"] + "\n"

    title = result["fields"]["summary"]
    return title, text
