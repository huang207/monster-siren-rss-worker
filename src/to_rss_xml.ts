import type { Song, AlbumData } from "./types";

export function toRssXml(albumData: AlbumData, newFeedUrl?: string): string {
    const escape = (str: any) => String(str ?? '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]!));
    let rss = `<?xml version="1.0" encoding="UTF-8"?>\n`;
    rss += `<rss xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">\n`;
    rss += `<channel>\n`;
    rss += `<title>${escape(albumData.name)}</title>\n`;
    rss += `<description>${escape(albumData.intro)}</description>\n`;
    rss += `<link>https://monster-siren.hypergryph.com/music</link>\n`;
    rss += `<copyright>${escape(albumData.belong)}</copyright>\n`;
    rss += `<language>zh-CN</language>\n`;
    if (newFeedUrl) {
        rss += `<itunes:new-feed-url>${escape(newFeedUrl)}</itunes:new-feed-url>\n`;
    }
    rss += `<itunes:explicit>clean</itunes:explicit>\n`;
    rss += `<itunes:type>serial</itunes:type>\n`;
    rss += `<itunes:summary>${escape(albumData.intro)}</itunes:summary>\n`;
    rss += `<itunes:author>${escape(albumData.artistes)}</itunes:author>\n`;
    rss += `<itunes:owner><itunes:name>塞壬唱片-MSR</itunes:name><itunes:email>monstersirenrecords@hypergryph.com</itunes:email></itunes:owner>\n`;
    rss += `<itunes:image href="${escape(albumData.cover)}"/>\n`;
    rss += `<itunes:category text="Music"/>\n`;
    for (let i = 0; i < albumData.songs.length; i++) {
        const song = albumData.songs[i];
        rss += `<item>`;
        rss += `<title>${escape(song.name)}</title>`;
        rss += `<guid isPermaLink="false">https://monster-siren.hypergryph.com/music/${escape(song.id)}</guid>`;
        rss += `<enclosure url="${escape(song.url)}"/>`;
        rss += `<itunes:explicit>clean</itunes:explicit>`;
        if (song.desc) {
            rss += `<description>${escape(song.desc)}</description>`;
        }
        if (song.cover) {
            rss += `<itunes:image href="${escape(song.cover)}"/>`;
        }
        if (song.pubDate) {
            rss += `<pubDate>${song.pubDate.toUTCString()}</pubDate>`;
        }
        rss += `<itunes:duration>0</itunes:duration>`;
        if (song.order) {
            rss += `<itunes:episode>${song.order}</itunes:episode>`;
        } else {
            rss += `<itunes:episode>${i + 1}</itunes:episode>`;
        }
        rss += `</item>\n`;
    }
    rss += `</channel>\n</rss>`;
    return rss;
}
