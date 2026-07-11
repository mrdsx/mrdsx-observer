from fastapi import status
from httpx import AsyncClient

from src.core.settings import Settings

settings = Settings()
IP_SERVICE_URL = "https://2ip.ru"


class GitHubWebhookService:
    async def update_webhook(self, http_client: AsyncClient) -> None:
        ip_headers = {"User-Agent": "curl/8.x.x"}
        ip_response = await http_client.get(IP_SERVICE_URL, headers=ip_headers)
        ip = ip_response.text.replace("\n", "")
        print(f"Updating webhook URL to {ip}:{settings.github_webhook_port}")

        github_headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "Authorization": f"Bearer {settings.github_api_token}",
        }
        webhook_data = {
            "content_type": "json",
            "url": f"http://{ip}:{settings.github_webhook_port}/webhook",
        }
        api_response = await http_client.patch(
            settings.update_webhook_url,
            headers=github_headers,
            json=webhook_data,
        )

        if api_response.status_code != status.HTTP_200_OK:
            raise Exception("Failed to update webhook")
