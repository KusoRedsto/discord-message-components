# discord.py button docs

> These are some docs for the discord.py button extension

- [Initializing](#GetStarted)
- [Client Events](#Events)
- [Sending Butttons](#Sending)
- [Receiving a button press](#Receiving)
- [Complete example](#Example)
- [Code docs](#CodeDocs)
- [Future added](#Future)

- - - -

# GetStarted

At first, you need a `discord.ext.commands.Bot` client

```py
import discord
from disicord.ext import commands

client = commands.Bot()
```

To initialize the Button extension, you need to import the `Buttons` class

```py
from discord_py_buttons import Buttons

client.buttons = Buttons(client)

```

This will add a listener to button presses and will grant you acces to the button tools

- - - -

# Events

These events can be received trought `client.listen('eventName')`

`'on_button_press'`

This event will be dispatched if a user pressed a button (a new interaction was created)

The parameters passed to your function will be

- `PressedButton`
    > The Button which was pressed


- `Message`
    > The message on which the button was pressed

Your function should look something like this
```py
@client.listen('on_button_press')
async def on_button(btn: PressedButton, messaeg: ResponseMessage)
    # code goes here
```

- - - -

# Sending

To send a button message, you need the `send` function from a `Buttons` instance

Example:
```py
from discord_py_buttons import Button

@client.listen('on_message')
async def on_message(message: discord.Message):
    if message.content == "!btn":
        client.buttons.send(message.channel, "here you go", buttons=[Button("myID", "Press me", emoji="😀")])
```

- - - -

# Receiving

If you want to receive a button press, you need to listen to the `on_button_press` event witht `client.listen('on_button_press')`


There will be two parameters which will be passed to your function

- `PressedButton`
    > The button which was pressed

- `ResponseMessage`
    > The message on which the button was pressed

To respond to the interaction, you use `theResponseMessage.respond()`

Example:
```py
@client.listen('on_button_press')
async def on_button(btn: PressedButton, msg: ResponseMsg):
    btn.respond("You pressed " + btn.content)
```

- - - -

# Example

Here is an example code, which sends a button everytime a user sends a message with the content `!btn` and replies to every button press with the content of the button

```py
import discord
from discord.ext import commands
from discord_py_buttons import Buttons, Button, PressedButton, ResponseMessage

client.buttons = Buttons(client)

@client.listen('on_message')
async def on_message(message: discord.Message):
    if message.content == "!btn":
        client.buttons.send("Here ya go!", buttons=[Button("custom_id", "PRESS ME")])
    
@client.listen('on_button_press')
async def on_button(btn: PressedButton, msg: ResponseMessage):
    msg.respond("You pressed on " + btn.content + " with the customID " + btn.custom_id)

client.login("Your secret token")
```

- - - -

- - - -

- - - -

# CodeDocs


## Buttons: `class`

A button instance for using buttons

<details>
<summary><b>Initialization</b></summary>

```py
Buttons(client: discord.ext.commands.client)
```

- client: `discord.ext.commands.client`
    > The bot client
</details>


<details>
<summary><b>Methods</b></summary>

-   <details>
    <summary><b>send</b></summary>

    ```py
    async def send(self, channel: discord.TextChannel, content=None, *, tts=False,
                embeds=None, file=None, files=None, delete_after=None, nonce=None,
                allowed_mentions=None, reference=None, mention_author=None, buttons=None
            ) -> Message:
    ```

    _| coroutine |_

    #### **Parameters**

    - channel: `discord.TextChannel`
        > The textchannel where the message should be sent
        __Required__

    - content: `str`
        > The text content of the message

    - tts: `bool`
        > If the message should be text-to-speech

    - embeds: `List[discord.Embed]`
        > The embeds included in the message

    - file: `discord.File`
        > A file sent as attachment

    - file: `List[discord.File]`
        > A list of files sent as attachment

    - delete_after: `float`
        > The numbers of seconds after which the message will be deleted in the background

    - nonce: `int`
        > The nonce to use for sending this message

    - allowed_mentions: `discord.Allowed_mentions`
        > Mentions allowed in this message

    - reference: `discord.MessageReference`
        > The reference to which the message replies

    - mention_author: `bool`
        > Whether the author should be mentioned

    - buttons: `List[Button]`
        > A list of buttons in this message


    #### **Returns**
    - `Message`
        > The sent message
    </details>
</details>

- - - -

## Button: `class`

Represents a message component button

<details>
<summary><b>Initialization</b></summary>
```py
Button(custom_id: str, label: str, color: str or int, emoji: discord.Emoji or str, new_line: bool, disabled: bool)
```

- custom_id: `str`
    > A customtID for identifying the button, max _100_ characters

- label: `str`
    > The text that appears on the button, max _80_ characters

- color: `str or int`
    > The color of the button, one of: 
    `[("blurple", "primary", 1), ("gray", "secondary", 2), ("green", "succes", 3), ("red", "danger", 4)]`
    Things in () are the same color

- emoji: `discord.Emoji or str`
    > A emoji appearing before the label

- new_line: `bool`
    > Whether a new line should be added before the button

- disabled: `bool`
    > Whether the button should be clickable (disabled = False) or not (disabled=True)
</details>

<details>
<summary><b>Attributes</b></summary>

- content: `str`
    > The content of the button (emoji + " " + label)

- custom_id: `str`
    > A customtID for identifying the button, max _100_ characters

- label: `str`
    > The text that appears on the button, max _80_ characters

- color: `str or int`
    > The color of the button

- emoji: `discord.Emoji or str`
    > The emoji appearing before the label

- new_line: `bool`
    > Whether a new line was added before the button

- disabled: `bool`
    > Whether the button is disabled
</details>

<details>
<summary><b>Methods</b></summary>

-   <details>
    <summary>to_dict: <code>function -> dict</code></summary>
    Converts the button to a python dictionary
    </details>
</details>

- - - -

## LinkButton: `class`

Represents a message component button that will open a link on click

This type of button will not trigger the `on_button_press` event


<details>
<summary><b>Initialization</b></summary>
```py
LinkButton(url: str, label: str, emoji: discord.Emoji or str, new_line: bool, disabled: bool)
```

- url: `str`
    > The url which will be opened when clicking the button

- label: `str`
    > The text that appears on the button, max _80_ characters

- emoji: `discord.Emoji or str`
    > A emoji appearing before the label

- new_line: `bool`
    > Whether a new line should be added before the button

- disabled: `bool`
    > Whether the button should be clickable (disabled = False) or not (disabled=True)
</details>

<details>
<summary><b>Attributes</b></summary>

- content: `str`
    > The content of the button (emoji + " " + label)

- url: `str`
    > The link which will be opened when clicking the button

- label: `str`
    > The text that appears on the button, max _80_ characters

- color: `str or int`
    > The color of the button

- emoji: `discord.Emoji or str`
    > The emoji appearing before the label

- new_line: `bool`
    > Whether a new line was added before the button

- disabled: `bool`
    > Whether the button is disabled
</details>

<details>
<summary><b>Methods</b></summary>

-   <details>
    <summary>to_dict: <code>function -> dict</code></summary>
    Converts the button to a python dictionary
    </details>
</details>

- - - -

## <a name="Message"></a> Message: `class`

Extends the `discord.Message` object


<details>
<summary><b>Attributes</b></summary>

- buttons: `List[Button or LinkButton]`
    > A list of buttons included in the message
</details>

<details>
<summary><b>Super</b></summary>
    <a href="https://discordpy.readthedocs.io/en/stable/api.html?highlight=message#discord.Message">discord.Message properties</a>
</details>

<br>

## ResponseMessage: `class`

A class for interaction responding to a message

Extends the `Message` object

<details>
<summary><b>Attributes</b></summary>

- pressedButton: `Button`
    > The button which was pressed
</details>

<details>
<summary><b>Methods</b></summary>

-   <details>
    <summary>acknowledge: <code>function</code></summary>
    Acknowledges that the interaction was receives, should be used if you need more than 15 seconds to responod
    </details>

-   <details>
    <summary>respond: <code>function</code></summary>
    Responds to the interaction

    ```py
    def respond(self, content=None, *, tts=False,
            embeds=None, file=None, files=None, nonce=None,
            allowed_mentions=None, reference=None, mention_author=None, buttons=None,
        ninjaMode = False):
    ```

    #### **Parameters**

    - content: `str`
        > The text content of the message

    - tts: `bool`
        > If the message should be text-to-speech

    - embeds: `List[discord.Embed]`
        > The embeds included in the message

    - file: `discord.File`
        > A file sent as attachment

    - files: `List[discord.File]`
        > A list of files sent as attachment

    - nonce: `int`
        > The nonce to use for sending this message
    
    - allowed_mentions: `discord.Allowed_mentions`
        > Mentions allowed in this message

    - reference: `discord.MessageReference`
        > The reference to which the message replies

    - mention_author: `bool`
        > Whether the author should be mentioned

    - buttons: `List[Button]`
        > A list of buttons in this message
    </details>
</details>

<details>
<summary><b>Super</b></summary>
    <a href="#-message-class">Message properties</a>
</details>

- - - -

<details>
    <summary><h2>Future</h2></summary>

- [ ] file sending complete support
- [ ] fixing function pararmeters
    - [ ] ResonseMessage.reply() add mention_author
- [ ] change `embed` to `embeds` 
- [ ] inline => new_line
</details>