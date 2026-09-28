"""Runtime environment and image-generation route policy."""

from __future__ import annotations

def infer_image_generation_route(environment: str, explicit_route: str | None) -> str:
    if explicit_route:
        return explicit_route
    if environment == "chatgpt_web":
        return "chatgpt_create_image"
    if environment == "codex":
        return "codex_imagegen"
    if environment in {"claude_code", "other"}:
        return "user_supplied_api_required"
    return "unknown"

def default_image_generation_note(environment: str) -> str:
    if environment == "codex":
        return "Codex must use Image Gen for every target-paper sketch, formal candidate, and approved rerun image; generate each image separately."
    if environment == "chatgpt_web":
        return "ChatGPT web must use Create Image with ChatGPT Images 2.0 for every target-paper sketch, formal candidate, and approved rerun image; generate each image separately."
    if environment in {"claude_code", "other"}:
        return (
            "Use an approved image generation API only when Codex Image Gen and ChatGPT web Create Image are unavailable; record the API name, reason, and limitations."
        )
    return "Resolve the image route before image steps: Codex Image Gen first, ChatGPT web Create Image / Images 2.0 second, otherwise an approved image API. Generated web-page routes are not used."

def runtime_environment_note(environment: str) -> str:
    if environment == "codex":
        return "Codex uses text replies plus direct Markdown image embeds for saved atlas boards; generated web pages are not produced."
    if environment == "chatgpt_web":
        return "ChatGPT web uses text replies plus direct Markdown image embeds for saved atlas boards; generated web pages are not produced."
    return "Use text replies plus direct atlas-board image embeds when package assets are available; generated web pages are not produced."


