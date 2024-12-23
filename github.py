import requests

class GithubConfig:
    def __init__(self):
        self.github_token = None
        self.github_repo = None

    def configure_github(self, token, repo):
        self.github_token = token
        self.github = repo

    def validate_github_config(self):
        if not self.github_token:
            raise ValueError("El token de GitHub no está configurado.")
        if not self.github_repo:
            raise ValueError("El repositorio no está configurado.")


# Singleton instance for global configuration
config = GithubConfig()


def comment_on_pr(pr_id, comment_body, cfg=config):
    """
    Comenta en un Pull Request en GitHub.

    :param pr_id: Número del Pull Request
    :param comment_body: Texto del comentario
    :param cfg: Instancia de configuración de GitHub
    """
    cfg.validate_github_config()
    
    url = f"https://api.github.com/repos/{cfg.github_repo}/issues/{pr_id}/comments"
    payload = {"body": comment_body}
    headers = {
        "Authorization": f"Bearer {cfg.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def get_pr_details(pr_id, cfg=config):
    """
    Obtiene detalles de un Pull Request en GitHub.

    :param pr_id: Número del Pull Request
    :param cfg: Instancia de configuración de GitHub
    """
    cfg.validate_github_config()
    
    url = f"https://api.github.com/repos/{cfg.github_repo}/pulls/{pr_id}"
    headers = {
        "Authorization": f"Bearer {cfg.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_file_content_from_pr(pr_id, file_path, cfg=config):
    """
    Obtiene el contenido de un archivo específico en un Pull Request.

    :param pr_id: Número del Pull Request
    :param file_path: Ruta del archivo en el PR
    :param cfg: Instancia de configuración de GitHub
    """
    cfg.validate_github_config()
    
    pr_details = get_pr_details(pr_id, cfg)
    head_sha = pr_details["head"]["sha"]
    
    url = f"https://api.github.com/repos/{cfg.github_repo}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {cfg.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {"ref": head_sha}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


'''
if __name__ == "__main__":
    config.configure_github(
        token="your_github_token",
        repo_owner="owner_name",
        repo_name="repo_name"
    )
    
    try:
        # Comentar en un PR
        response = comment_on_pr(1, "This is a test comment from Github Bot.")
        print("Comentario añadido:", response)

        # Obtener detalles de un PR
        pr_details = get_pr_details(1)
        print("Detalles del PR:", pr_details)

        # Obtener contenido de un archivo en el PR
        file_content = get_file_content_from_pr(1, "path/to/file.py")
        print("Contenido del archivo:", file_content)

    except Exception as e:
        print("Error:", e)
'''