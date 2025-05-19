from urllib.parse import urlparse, urlunparse, parse_qs
from workers import Request, Response
from get_album import get_album
from to_rss_xml import to_rss_xml


class Router:
    def __init__(self, request: Request):
        self.routes = {}
        self.url = request.url
        self.path = urlparse(request.url.lower()).path
        self.command = request.method
        self.headers = request.headers
        self.query = parse_qs(urlparse(request.url.lower()).query)
        self.body = request.body

        self.not_found = Response("Not Found", status=404)

    async def do_GET(self):
        try:
            if self.path == "/rss":
                if "albumid" in self.query:
                    return Response(
                        to_rss_xml(await get_album(self.query["albumid"][0])).toxml(),
                        headers={"Content-Type": "application/rss+xml;charset=UTF-8"},
                    )
                else:
                    return Response("Invalid Request", status=400)
            if self.path == "/":
                if "albumid" in self.query:
                    return Response(
                        to_rss_xml(
                            await get_album(self.query["albumid"][0]),
                            urlunparse(urlparse(self.url)._replace(path="/rss")),
                        ).toxml(),
                        headers={"Content-Type": "application/rss+xml;charset=UTF-8"},
                    )
                else:
                    return Response("Invalid Request", status=400)
            else:
                return self.not_found
        except Exception as e:
            raise e

    async def handle(self):
        try:
            if self.command == "GET":
                return await self.do_GET()
            else:
                return self.not_found
        except Exception as e:
            return Response(f"Error: {e}", status=500)


async def on_fetch(request, env):
    route = Router(request)
    return await route.handle()
