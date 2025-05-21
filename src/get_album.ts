import type { Song, AlbumData } from "./types";

const urls = {
    getAlbums: () => `https://monster-siren.hypergryph.com/api/albums`,
    getAlbumData: (id: string) => `https://monster-siren.hypergryph.com/api/album/${id}/data`,
    getAlbumDetail: (id: string) =>
        `https://monster-siren.hypergryph.com/api/album/${id}/detail`,
    getSongs: () => `https://monster-siren.hypergryph.com/api/songs`,
    getSong: (id: string) => `https://monster-siren.hypergryph.com/api/song/${id}`,
}

export async function get_album(album_id: string) {
    // Get the datas of the album
    var response = await fetch(urls.getAlbumData(album_id));
    if (!response.ok) {
        throw new Error(`Failed to fetch album data: ${response.statusText}`);
    }
    var json_data: any = await response.json();
    const album_datas = json_data['data'];

    if ((!('code' in json_data)) || json_data['code'] !== 0) {
        throw new Error(`Failed to fetch album data: ${album_id}`);
    }

    // Get the details of the album
    response = await fetch(urls.getAlbumDetail(album_id));
    if (!response.ok) {
        throw new Error(`Failed to fetch album details: ${response.statusText}`);
    }
    json_data = await response.json();
    const album_details = json_data['data'];

    if ((!('code' in json_data)) || json_data['code'] !== 0) {
        throw new Error(`Failed to fetch album details: ${album_id}`);
    }

    const album_name = album_details['name'];
    const album_cover = album_details['coverUrl'];
    const ablum_artistes = (album_datas['artistes'] as string[]).join(", ");

    var album_data: AlbumData = {
        album_id: album_id,
        name: album_name,
        artistes: ablum_artistes,
        intro: album_details["intro"],
        belong: album_details["belong"],
        cover: album_cover,
        songs: [],
    };

    // Iterate through each song in the album and get its details
    for (const song of album_details['songs']) {
        const song_id = song['cid'];
        const song_name = song['name'];
        const song_artistes = (song['artistes'] as string[]).join(", ");
        const song_url = urls.getSong(song_id);

        // Get the details of the song
        response = await fetch(urls.getSong(song_id));
        if (!response.ok) {
            throw new Error(`Failed to fetch song details: ${response.statusText}`);
        }
        json_data = await response.json();
        const song_details = json_data['data'];

        if ((!('code' in json_data)) || json_data['code'] !== 0) {
            continue;
        }

        // const pubDateRegex = /\/(\d{4})(\d{2})(\d{2})\//;
        // const pubDateMatch = pubDateRegex.exec(song_details['sourceUrl']);
        // const pubDate = pubDateMatch ? new Date(`${pubDateMatch[1]}-${pubDateMatch[2]}-${pubDateMatch[3]}T00:00:00+0800`) : null;
        let pubDate: Date | null = null;
        let contentType: String | null = null;
        let contentLength: number | null = null;
        const headResp = await fetch(song_details['sourceUrl'], { method: "HEAD" });
        if (headResp.ok) {
            contentType = headResp.headers.get("Content-Type");
            contentLength = parseInt(headResp.headers.get("Content-Length") ?? "0");
            const lastModified = headResp.headers.get("Last-Modified");
            if (lastModified) {
                pubDate = new Date(lastModified);
            }
        }

        album_data["songs"].push({
            id: song_id,
            name: song_name,
            artistes: song_artistes,
            pubDate: pubDate ?? undefined,
            url: song_details['sourceUrl'],
            contentType: contentType ?? undefined,
            contentLength: contentLength ?? undefined,
            lyric: song_details['lyricUrl'],
        });
    }

    return album_data;
}