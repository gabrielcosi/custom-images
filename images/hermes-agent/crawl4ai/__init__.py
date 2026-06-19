import logging
import os
import re
from typing import Any, Dict, List

import httpx

from agent.web_search_provider import WebSearchProvider

logger = logging.getLogger(__name__)
_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


class Crawl4aiWebSearchProvider(WebSearchProvider):
    @property
    def name(self) -> str:
        return "crawl4ai"

    @property
    def display_name(self) -> str:
        return "Crawl4AI"

    def is_available(self) -> bool:
        return bool(os.getenv("CRAWL4AI_API_URL", "").strip())

    def supports_search(self) -> bool:
        return False

    def supports_extract(self) -> bool:
        return True

    def extract(self, urls: List[str], **kwargs: Any) -> List[Dict[str, Any]]:
        base = os.getenv("CRAWL4AI_API_URL", "").strip().rstrip("/")
        flt = os.getenv("CRAWL4AI_FILTER", "fit").strip() or "fit"

        def fail(url: str, msg: str) -> Dict[str, Any]:
            return {"url": url, "title": "", "content": "", "raw_content": "", "error": msg, "metadata": {"sourceURL": url}}

        if not base:
            return [fail(u, "CRAWL4AI_API_URL not set") for u in urls]

        headers = {"content-type": "application/json"}
        token = os.getenv("CRAWL4AI_TOKEN", "").strip()
        if token:
            headers["Authorization"] = f"Bearer {token}"

        out: List[Dict[str, Any]] = []
        for url in urls:
            try:
                resp = httpx.post(f"{base}/md", json={"url": url, "f": flt}, headers=headers, timeout=120)
                resp.raise_for_status()
                data = resp.json()
            except httpx.HTTPError as exc:
                logger.warning("crawl4ai extract %s: %s", url, exc)
                out.append(fail(url, f"crawl4ai extract failed: {exc}"))
                continue
            if not data.get("success", True):
                out.append(fail(url, str(data.get("error", "extraction failed"))))
                continue
            md = data.get("markdown", "")
            if isinstance(md, dict):
                md = md.get("fit_markdown") or md.get("raw_markdown") or ""
            md = md or ""
            heading = _H1.search(md)
            title = heading.group(1).strip() if heading else ""
            out.append({"url": url, "title": title, "content": md, "raw_content": md, "metadata": {"sourceURL": url, "title": title}})
        return out


def _teach_web_tools_gate() -> None:
    try:
        import tools.web_tools as wt
    except Exception:
        return
    orig = getattr(wt, "_is_backend_available", None)
    if orig is None or getattr(orig, "_crawl4ai_wrapped", False):
        return

    def _is_backend_available(backend: str) -> bool:
        if backend == "crawl4ai":
            return bool(os.getenv("CRAWL4AI_API_URL", "").strip())
        return orig(backend)

    _is_backend_available._crawl4ai_wrapped = True
    wt._is_backend_available = _is_backend_available


def register(ctx) -> None:
    ctx.register_web_search_provider(Crawl4aiWebSearchProvider())
    _teach_web_tools_gate()
