import os
import shutil
import tempfile
from pathlib import Path


def _patch_streamlit_static_assets() -> None:
    if os.environ.get("DRAFTAI_STATIC_PATCHED") == "1":
        return

    try:
        from streamlit import file_util
    except Exception:
        return

    static_src = Path(file_util.get_static_dir())
    if not static_src.exists():
        return

    candidates = [
        Path.cwd() / "favicon.png",
        Path.cwd() / "engineering-drawing-reader" / "favicon.png",
        Path(__file__).resolve().parent / "favicon.png",
        Path(__file__).resolve().parent.parent / "favicon.png",
    ]
    favicon_src = next((p for p in candidates if p.exists()), None)
    if favicon_src is None:
        return

    temp_root = Path(tempfile.mkdtemp(prefix="draftai-static-"))
    static_dst = temp_root / "static"
    shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
    shutil.copyfile(favicon_src, static_dst / "favicon.png")

    index_html = static_dst / "index.html"
    if index_html.exists():
        html = index_html.read_text(encoding="utf-8")
        html = html.replace("<title>Streamlit</title>", "<title>Draft AI</title>")
        index_html.write_text(html, encoding="utf-8")

    file_util.get_static_dir = lambda: str(static_dst)
    os.environ["DRAFTAI_STATIC_PATCHED"] = "1"


_patch_streamlit_static_assets()
