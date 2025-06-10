# Monster Siren RSS Worker

A simple Cloudflare Worker that generates a podcast RSS feed for [Monster Siren Recored](https://monster-siren.hypergryph.com/).
> [Monster Siren Recored](https://monster-siren.hypergryph.com/) is the official site for the original soundtracks (OST) from the game Arknights.

## Usage

1. Deploy the worker on your Cloudflare dashboard.
2. Get `cid` of the album you want.
   - On Windows, you can use the PowerShell command:

     ```powershell
     ((Invoke-WebRequest -Uri https://monster-siren.hypergryph.com/api/albums | Select -ExpandProperty Content | ConvertFrom-Json).data | Where-Object {$_.name -eq "Album name"}).cid
     ```

     > Replace `Album name` with the name of the album you want.

3. Add `https://[your-worker-url]/rss?albumId=[cid]` to your podcast app.
