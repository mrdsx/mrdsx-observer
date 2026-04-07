from src.core.settings import get_settings

settings = get_settings()

service_account: dict[str, str] = {
    "type": "service_account",
    "project_id": "mrdsx-observer",
    "private_key": settings.firebase_private_key.replace("\\n", "\n"),
    "client_email": "firebase-adminsdk-fbsvc@mrdsx-observer.iam.gserviceaccount.com",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40classic-word-game.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}
