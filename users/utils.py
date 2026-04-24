import re

def get_youtube_embed_url(url):
    """
    Extracts the YouTube Video ID and returns a clean embed URL.
    The security parameters (origin, enablejsapi) are added in the template
    to ensure they match the browser's current address dynamically.
    """
    if not url:
        return ""

    # Precise 11-char ID extraction
    regex = r"(?:v=|youtu\.be\/|embed\/|watch\?v=|&v=)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)

    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"

    return url
