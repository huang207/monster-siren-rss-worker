from xml.dom import minidom

def to_rss_xml(album_data: dict) -> minidom.Document:
    """
    Convert the album data to RSS XML format.
    """
    # Create the RSS document
    doc = minidom.Document()
    rss = doc.createElement("rss")
    rss.setAttribute("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    rss.setAttribute("xmlns:itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
    rss.setAttribute("version", "2.0")
    doc.appendChild(rss)

    channel = doc.createElement("channel")
    rss.appendChild(channel)

    # Add the channel title and link
    title = doc.createElement("title")
    title.appendChild(doc.createTextNode(album_data["name"]))
    channel.appendChild(title)

    description = doc.createElement("description")
    description.appendChild(doc.createTextNode(album_data["intro"]))
    channel.appendChild(description)

    link = doc.createElement("link")
    link.appendChild(doc.createTextNode("https://monster-siren.hypergryph.com/music"))
    channel.appendChild(link)

    copyright = doc.createElement("copyright")
    copyright.appendChild(doc.createTextNode(album_data["belong"]))
    channel.appendChild(copyright)

    language = doc.createElement("language")
    language.appendChild(doc.createTextNode("zh-CN"))
    channel.appendChild(language)

    itunes_explicit = doc.createElement("itunes:explicit")
    itunes_explicit.appendChild(doc.createTextNode("clean"))
    channel.appendChild(itunes_explicit)

    itunes_type = doc.createElement("itunes:type")
    itunes_type.appendChild(doc.createTextNode("serial"))
    channel.appendChild(itunes_type)

    itunes_summary = doc.createElement("itunes:summary")
    itunes_summary.appendChild(doc.createTextNode(album_data["intro"]))
    channel.appendChild(itunes_summary)

    itunes_author = doc.createElement("itunes:author")
    itunes_author.appendChild(doc.createTextNode(album_data["artistes"]))
    channel.appendChild(itunes_author)

    itunes_owner = doc.createElement("itunes:owner")
    itunes_owner_name = doc.createElement("itunes:name")
    itunes_owner_name.appendChild(doc.createTextNode("塞壬唱片-MSR"))
    itunes_owner.appendChild(itunes_owner_name)
    itunes_owner_email = doc.createElement("itunes:email")
    itunes_owner_email.appendChild(doc.createTextNode("monstersirenrecords@hypergryph.com"))
    itunes_owner.appendChild(itunes_owner_email)
    channel.appendChild(itunes_owner)

    itunes_image = doc.createElement("itunes:image")
    itunes_image.setAttribute("href", album_data["cover"])
    channel.appendChild(itunes_image)

    itunes_category = doc.createElement("itunes:category")
    itunes_category.setAttribute("text", "Music")
    channel.appendChild(itunes_category)

    # Add each album as an item in the channel
    for order, song in enumerate(album_data["songs"]):
        item = doc.createElement("item")

        item_title = doc.createElement("title")
        item_title.appendChild(doc.createTextNode(song["name"]))
        item.appendChild(item_title)

        item_guid = doc.createElement("guid")
        item_guid.setAttribute("isPermaLink", "false")
        item_guid.appendChild(doc.createTextNode(f"https://monster-siren.hypergryph.com/music/{song["id"]}"))
        item.appendChild(item_guid)

        item_enclosure = doc.createElement("enclosure")
        item_enclosure.setAttribute("url", song["url"])
        item_enclosure.setAttribute("length", "0")
        item_enclosure.setAttribute("type", "audio/wav")
        item.appendChild(item_enclosure)

        item_itunes_explicit = doc.createElement("itunes:explicit")
        item_itunes_explicit.appendChild(doc.createTextNode("clean"))
        item.appendChild(item_itunes_explicit)

        item_itunes_image = doc.createElement("itunes:image")
        item_itunes_image.setAttribute("href", album_data["cover"])
        item.appendChild(item_itunes_image)

        item_itunes_duration = doc.createElement("itunes:duration")
        item_itunes_duration.appendChild(doc.createTextNode("0"))
        item.appendChild(item_itunes_duration)

        item_itunes_episode = doc.createElement("itunes:episode")
        item_itunes_episode.appendChild(doc.createTextNode(str(order + 1)))
        item.appendChild(item_itunes_episode)

        channel.appendChild(item)

    return doc
