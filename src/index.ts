/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Bind resources to your worker in `wrangler.jsonc`. After adding bindings, a type definition for the
 * `Env` object can be regenerated with `npm run cf-typegen`.
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */
import { get_album } from "./get_album";
import { toRssXml } from "./to_rss_xml";

class Router {
    private url: string;
    private path: string;
    private method: string;
    private headers: HeadersInit;
    private params: Record<string, string>;
    private body: string | null;

    constructor(request: Request) {
        this.url = request.url;
        this.path = new URL(request.url.toLowerCase()).pathname;
        this.method = request.method;
        this.headers = request.headers;
        this.params = Object.fromEntries(new URL(request.url.toLowerCase()).searchParams.entries());
        this.body = null;
    }

    async do_GET(): Promise<Response> {
        if (this.path === '/rss' || this.path === '/') {
            if ("albumid" in this.params) {
                try {
                    return new Response(toRssXml(await get_album(this.params["albumid"])), {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                }
                catch (error) {
                    console.error('Error fetching album:', error);
                    return new Response('Internal Server Error', { status: 500 });
                }
            }
            return new Response('Not Found', { status: 404 });
        }
        return new Response('Not Found', { status: 404 });
    }

    async handleRequest(): Promise<Response> {
        if (this.method === 'GET') {
            try {
                return await this.do_GET();
            }
            catch (error) {
                console.error('Error handling GET request:', error);
                return new Response('Internal Server Error', { status: 500 });
            }
        }
        return new Response('Not Found', { status: 404 });
    }
}
export default {
    async fetch(request, env, ctx): Promise<Response> {
        var route = new Router(request);
        var response = await route.handleRequest();
        if (response) {
            return response;
        }
        var respone = await fetch('https://monster-siren.hypergryph.com/api/album/9377/detail');
        return new Response(respone.body, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return new Response('Hello World!');
    },
} satisfies ExportedHandler<Env>;
