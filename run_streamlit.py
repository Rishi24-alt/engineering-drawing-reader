import os
import shutil
from pathlib import Path

from streamlit import file_util
from streamlit.web import bootstrap

APP_DIR = Path(__file__).resolve().parent
MAIN_SCRIPT = str(APP_DIR / "app.py")
APP_FAVICON = APP_DIR / "favicon.png"


def _toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _write_runtime_secrets_from_env():
    """
    Build `.streamlit/secrets.toml` from env vars (useful on Railway).
    This keeps secrets out of git while still enabling Streamlit auth.
    """
    secrets_dir = APP_DIR / ".streamlit"
    secrets_path = secrets_dir / "secrets.toml"

    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    proxy_url = os.getenv("PROXY_URL", "https://api.openai.com").strip()

    auth_redirect_uri = os.getenv("AUTH_REDIRECT_URI", "").strip()
    auth_cookie_secret = os.getenv("AUTH_COOKIE_SECRET", "").strip()
    google_client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
    google_metadata_url = os.getenv(
        "GOOGLE_SERVER_METADATA_URL",
        "https://accounts.google.com/.well-known/openid-configuration",
    ).strip()

    lines = []
    if openai_api_key:
        lines.append(f'OPENAI_API_KEY = "{_toml_escape(openai_api_key)}"')
    if proxy_url:
        lines.append(f'PROXY_URL = "{_toml_escape(proxy_url)}"')

    has_google_auth = all(
        [
            auth_redirect_uri,
            auth_cookie_secret,
            google_client_id,
            google_client_secret,
            google_metadata_url,
        ]
    )
    if has_google_auth:
        lines.extend(
            [
                "",
                "[auth]",
                f'redirect_uri = "{_toml_escape(auth_redirect_uri)}"',
                f'cookie_secret = "{_toml_escape(auth_cookie_secret)}"',
                "",
                "[auth.google]",
                f'client_id = "{_toml_escape(google_client_id)}"',
                f'client_secret = "{_toml_escape(google_client_secret)}"',
                f'server_metadata_url = "{_toml_escape(google_metadata_url)}"',
            ]
        )

    if not lines:
        return

    secrets_dir.mkdir(parents=True, exist_ok=True)
    secrets_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _prepare_custom_static_dir() -> Path:
    base_static_dir = Path(file_util.get_static_dir())
    runtime_root = APP_DIR / ".runtime_static"
    custom_static_dir = runtime_root / "static"
    if runtime_root.exists():
        shutil.rmtree(runtime_root, ignore_errors=True)
    runtime_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base_static_dir, custom_static_dir, dirs_exist_ok=True)

    if APP_FAVICON.exists():
        shutil.copyfile(APP_FAVICON, custom_static_dir / "favicon.png")

    return custom_static_dir


CUSTOM_STATIC_DIR = _prepare_custom_static_dir()
_write_runtime_secrets_from_env()
file_util.get_static_dir = lambda: str(CUSTOM_STATIC_DIR)

flag_options = {
    "server_headless": True,
    "server_port": int(os.getenv("PORT", "8501")),
    "server_address": "0.0.0.0",
    "server_fileWatcherType": "none",
    "browser_gatherUsageStats": False,
}

bootstrap.run(MAIN_SCRIPT, False, [], flag_options)
