import requests
from . import buttons

url = "https://discord.com/api/v8"

def POST(token, url, data):
    return requests.post(url,
        json=data, headers={"Authorization": f"Bot {token}"})
def GET(token, url):
    return requests.get(url,
        headers={"Authorization": f"Bot {token}"})
def DELETE(token, url):
    return requests.delete(url,
        headers={"Authorization": f"Bot {token}"})

def jsonifyMessage(content=None, *, tts=False, embed=None, file=None, files=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None, buttons=None):
    json = { }
    if content != None:
        json |= { "content": content }
    if tts == False:
        json |= { "tts": tts }
    if file != None:
        json |= { "file": file }
    if files != None:
        json |= {"files": files}
    if nonce != None:
        json |= { "nonce": nonce }
    if allowed_mentions != None:
        json |= { "mentions" }

    #region embed
    if embed != None:
        embedJSON = {"embed": {"type": "rich"} }

        if embed.title:
            embedJSON["embed"] |= embedJSON["embed"] | {"title": embed.title}
        if embed.description:
            embedJSON["embed"] |= {"description": embed.description}
        if embed.url:
            embedJSON["embed"] |= {"url": embed.url}
        if embed.timestamp:
            embedJSON["embed"] |= {"timestamp": embed._timestamp}
        if embed.color:
            embedJSON["embed"] |= {"color": embed._colour.value}
        if embed.footer:
            embedJSON["embed"] |= {"footer": embed._footer}
        if embed.image:
            embedJSON["embed"] |= {"image": embed._image}
        if embed.thumbnail:
            embedJSON["embed"] |= {"thumbnail": embed._thumbnail} 
        if embed.video:
            embedJSON["embed"] |= {"video": embed.video}
        if embed.provider:
            embedJSON["embed"] |= {"provider": embed.provider}
        if embed.author:
            embedJSON["embed"] |= {"author": embed._author}
        if embed.fields:
            embedJSON["embed"] |= {"fields": embed._fields}
        if embed.thumbnail:
            embedJSON["embed"] |= {"thumbnail": embed._thumbnail}

        json = json | embedJSON
    #endregion
    #region reference
    if reference:
        json |= {"message_reference": {"message_id": reference.id if type(reference) == discord.Message else reference}}
    #endregion
    #region buttons
    if buttons:
        componentsJSON = {"components": []}
        
        wrapperButtons: List[List[buttons.Button]] = []
        currentLineButtons: List[buttons.Button] = []

        if len(buttons) > 1:
            for btn in buttons:
                if(len(currentLineButtons) > 5):
                    raise Exception("Limit exceeded: Max. 5 Buttons in a row")
                if btn.inline:
                    currentLineButtons.append(btn)
                else:
                    if(len(currentLineButtons) > 0):
                        wrapperButtons.append(currentLineButtons)
                    wrapperButtons.append([btn])
                    currentLineButtons = []
            if(len(currentLineButtons) > 0):
                wrapperButtons.append(currentLineButtons)
        else:
            wrapperButtons.append([buttons[0]])

        for lineButtons in wrapperButtons:
            lineButtons: List[Button] = lineButtons
            componentsJSON["components"].append({"type": 1, "components": [x._json for x in lineButtons]})

        json |= componentsJSON
    #endregion buttons

    return json