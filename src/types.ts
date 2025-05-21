// 公共类型定义文件
export type Song = {
    id: any;
    order?: number | string;
    name: any;
    artistes?: string;
    desc?: string;
    pubDate?: Date;
    cover?: string;
    url: any;
    lyric: any;
};

export type AlbumData = {
    album_id: string;
    name: string;
    artistes: string;
    intro: any;
    belong: any;
    cover: any;
    songs: Song[];
};
