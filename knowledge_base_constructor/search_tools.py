import re
import time

from ddgs import DDGS
from langchain_core.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi


def _ddg_text(query: str, max_results: int = 5, retries: int = 3) -> list[dict]:
    """DDG free-tier search occasionally rate-limits under parallel load, so retry with backoff."""
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return DDGS().text(query, max_results=max_results)
        except Exception as exc:
            last_error = exc
            time.sleep(2 * (attempt + 1))
    raise last_error


def _format_results(results: list[dict]) -> str:
    if not results:
        return "No results found."
    entries = []
    for r in results:
        title = r.get("title", "")
        url = r.get("href") or r.get("url", "")
        body = r.get("body", "")
        entries.append(f"Title: {title}\nURL: {url}\nSnippet: {body}")
    return "\n\n".join(entries)


@tool
def web_search_tool(query: str) -> str:
    """Searches the web for general articles and news about a topic.

    Args:
        query (str): the search query

    Returns:
        str: titles, URLs and snippets of the top results
    """
    try:
        results = _ddg_text(query)
    except Exception as exc:
        return f"Search failed: {exc}"
    return _format_results(results)


@tool
def interview_search_tool(query: str) -> str:
    """Searches the web specifically for written interviews and interview transcripts.

    Args:
        query (str): the search query, should already mention the person's name

    Returns:
        str: titles, URLs and snippets of the top results
    """
    try:
        results = _ddg_text(f"{query} interview transcript")
    except Exception as exc:
        return f"Search failed: {exc}"
    return _format_results(results)


@tool
def youtube_search_tool(query: str) -> str:
    """Searches YouTube for videos (interviews, talks, appearances) about a topic.

    Args:
        query (str): the search query, should already mention the person's name

    Returns:
        str: titles and URLs of matching YouTube videos
    """
    try:
        results = _ddg_text(f"{query} site:youtube.com")
    except Exception as exc:
        return f"Search failed: {exc}"
    return _format_results(results)


_YOUTUBE_ID_RE = re.compile(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})")


@tool
def youtube_transcript_tool(video_url: str) -> str:
    """Fetches the transcript text of a YouTube video given its URL.

    Args:
        video_url (str): a youtube.com or youtu.be video URL

    Returns:
        str: the transcript text, or an error message if unavailable
    """
    match = _YOUTUBE_ID_RE.search(video_url)
    if not match:
        return f"Could not extract a video id from '{video_url}'."
    video_id = match.group(1)
    try:
        fetched = YouTubeTranscriptApi().fetch(video_id)
    except Exception as exc:
        return f"Transcript unavailable for {video_url}: {exc}"
    return " ".join(snippet.text for snippet in fetched)


article_tools = [web_search_tool]
interview_tools = [interview_search_tool]
video_tools = [youtube_search_tool, youtube_transcript_tool]
