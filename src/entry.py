from workers import Response
from urllib.parse import urlparse, parse_qs
from get_album import get_album
from to_rss_xml import to_rss_xml


async def on_fetch(request, env):
    queries = parse_qs(urlparse(request.url.lower()).query)
    if "albumid" in queries:
        try:
            return Response(
                to_rss_xml(await get_album(queries["albumid"][0])).toxml(),
                headers={"Content-Type": "application/rss+xml;charset=UTF-8"},
            )
        except Exception as e:
            return Response(f"Error: {e}", status=500)
    return Response("Invalid Request", status=400)
