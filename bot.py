import os
import sys
import time
import subprocess
from collections import defaultdict
from requests.auth import HTTPBasicAuth
import openai
from openai import ChatCompletion
import attlassian
from dotenv import load_dotenv
load_dotenv()

# Variables de entorno
BITBUCKET_PR_ID = os.getenv("BITBUCKET_PR_ID")
BITBUCKET_BRANCH = os.getenv("BITBUCKET_BRANCH")
BITBUCKET_PR_DESTINATION_BRANCH = os.getenv("BITBUCKET_PR_DESTINATION_BRANCH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def analyze_code_with_openai(content):
    response = ChatCompletion.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[{"role": "system", "content": "Tu eres un revisor de código"}, {"role": "user", "content": f"{content}"}],
    )
    return response.choices[0].message["content"]


def get_changed_files_from_diffbash(script_path, script_args):
    try:
        script_path = os.path.abspath(script_path)
        result = subprocess.run(["bash", script_path] + script_args, capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().splitlines()

        # Separar las diferencias por archivo
        changes_by_file = defaultdict(list)
        current_file = None

        for line in output_lines:
            if line.startswith("File:"):
                current_file = line.split("File: ", 1)[1]
            elif current_file and line.strip() and line != "---":
                changes_by_file[current_file].append(line)

        return dict(changes_by_file)

    except subprocess.CalledProcessError as e:
        print(f"Error executing script {script_path}: {e.stderr}")
        return {}

def get_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()
    
    
def get_issue_id_from_branch(branch_name):
    parts = branch_name.split("/")
    if len(parts) > 1:
        return parts[1]
    else:
        return ""


def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower()


def get_prompt_template_by_file_extention(ext):
    match ext:
        case ".cs":
            return "csharp-prompt"
        case ".php" | ".go":
            print(f"prompt for file -{ext}- not implemented ")
            sys.exit(1)
        case _:
            print(f"prompt for file -{ext}- not implemented ")
            sys.exit(1)


def main(file_extentions_included_args):
    prompt_base = get_file_content("prompts-templates/base-prompt.txt")
    prompt_result_base = get_file_content("prompts-templates/result-prompt.txt")

    print("envars:")
    print(BITBUCKET_PR_ID)
    print(BITBUCKET_PR_DESTINATION_BRANCH)
    print(BITBUCKET_BRANCH)
    print("\n\n")

    # pull request information
    pull_request_content = attlassian.get_content_on_pr_from_bitbucket(BITBUCKET_PR_ID)
    pr_commit_title = pull_request_content["title"]
    pr_commit_message = pull_request_content["description"]

    # jira issue information
    issue_id = get_issue_id_from_branch(BITBUCKET_BRANCH)
    issue_title, issue_text = attlassian.get_issue_from_jira(issue_id)

    # get changes by file
    files_changes = get_changed_files_from_diffbash(
        "diff.sh", [f"{BITBUCKET_PR_DESTINATION_BRANCH}", f"{BITBUCKET_BRANCH}", f"{file_extentions_included_args}"]
    )

    for file, diffs in files_changes.items():
        analysis_results = ""
        # format diff file changes
        file_changes = f"Código a revisar en el archivo {file} :\n\n"
        for diff in diffs:
            file_changes += f"{diff}\n"

        # get prompt by file type
        extension = get_file_extension(file)
        prompt_filename = get_prompt_template_by_file_extention(extension)
        prompt_template = get_file_content(f"prompts-templates/{prompt_filename}.txt")
        prompt_for_file = (
            prompt_base.replace("{{prompt}}", prompt_template)
            .replace("{{issue-text}}", issue_title + " - " + issue_text)
            .replace("{{commit-text}}", pr_commit_title + " - " + pr_commit_message)
            .replace("{{code-text}}", file_changes)
            .replace("{{result-prompt}}", prompt_result_base)
        )

        print(prompt_for_file)
        analysis_results = analyze_code_with_openai(prompt_for_file) + "\n\n"
        if analysis_results != "":
            response = attlassian.comment_on_pr_from_bitbucket(BITBUCKET_PR_ID, file, analysis_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bot.py  [file extention included ej. cs,php,txt]")
        sys.exit(1)

    file_extentions_included_args = sys.argv[1]
    main(file_extentions_included_args)
