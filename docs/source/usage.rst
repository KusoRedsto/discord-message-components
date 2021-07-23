=================
Usage
=================



Get started
=====================

At first, you need to import the discord.py package and this package

.. code-block::

    import discord
    from discord.ext import commands
    from discord_message_components import Components


Create a new discord client

.. code-block::

    client = commands.Bot(" ")

.. warning::

    Note that the discord client has to be of type :class:`discord.ext.commands.Bot`, or else it won't work

Then you need to create a new :class:`~Extension` instance, with which you can use message components and slash commands

.. code-block::

    extension = Extension(client)


Message-components
=====================

Sending
~~~~~~~~~~~~~~~~~~~~~~

To send a component, we need to acces our :class:`~Components` class with ``extension.components`` and use the ``.send()`` function of it 

In this example, we'll wait for a message with the content "!test"

.. code-block::

    @client.listen
    async def on_message(message):
        if message.content == "!test":
            ...

Now we will send a component to the text channel where the *"!test"* message came from

Let's say we want to send two buttons and a select menu

We need to import them at first. For that, we need to go back to the beginning, where we imported the module

.. code-block::

    import discord
    from discord.ext import commands
    from discord_message_components import Components, Button, SelectMenu, SelectOption

And to send them, we use

.. code-block::

    ...
    await message.channel.send(message.channel, "Hello World", components=[
        Button("my_custom_id", "press me", "green"),
        Button("my_other_custom_id", "or press me!", emoji="😁", new_line=True),
        SelectMenu("another_custom_id", options=[
                SelectOption("choose me", 1),
                SelectOption("or me", 2),
                SelectOption("or me", 3)
        ], placeholder="Select something")
    ])

The message

.. image:: images/components/hello_world_all_components.png
   :width: 1000

The select menu

.. image:: images/components/hello_world_all_components_select_menu.png
   :width: 1000

.. note::

    Instead of using `new_line=True`, you can either put all components you want to have in one line into a list

    .. code-block::

        components=[[Button(...), Button(...)], LinkButton(...)]


    or put them into an :class:`~ActionRow`

    .. code-block::

        components=[ActionRow(Button(...), Button(...)), LinkButton(...)]


Now that we sent some components, how do we receive them?

Receiving
~~~~~~~~~~~~~~~

To receive a button press or a selection, we can listen to the ``button_press`` and the ``menu_select`` events


**Button**

.. code-block::

    @client.listen('on_button_press')
    async def on_button(btn, message):
        # respond
        await btn.respond("you clicked on " + btn.content)

.. image:: images/components/press_button_example.gif
   :width: 600


To get the user who pressed the button, you use ``btn.member``.
If you want to acces the message on which the button is, you use ``messsage``

**Select menu**

.. code-block::

    @client.listen('on_menu_select')
    async def on_menu(menu, message):
        # respond
        await menu.respond("you selected " + ', '.join([value.content for value in menu.values]))
 
.. image:: images/components/select_menu_example.gif
   :width: 600

To get the user who selected a value, you use ``menu.member``.
To get the value(s) selected by the user, you need to acces ``menu.values``



And to respond to the component interaction as you could already see up there, we can use

.. code-block::

    await message.respond("we gotcha!")

or

.. code-block::

    async def on_component(component, message):
        await component.respond("yo")

where the ``component`` parameter the pressed button or the selected menu

 

Easier ways
~~~~~~~~~~~~

But there are some more ways to receive and respond to them

You can send a message and directly wait for a button press and respond to it

.. code-block::

    @client.listen
    async def on_message(message):
        if message.content == "!test":
            btn = await (
                await message.channel.send(message.channel, "hello", components=[
                    Button("custom_id", "there")
                ])
            ).wait_for("button")
            await btn.respond("you pressed a button")


And we got listening components with a function that will always be executed if a component with a special custom_id was pressed

.. code-block::

    @extension.components.listening_component(custom_id="listening")
    async def listening_component(component, message):
        await component.respond("we got a component in this")


    @client.listen
    async def on_message(message):
        if message.content == "!test":
            await message.channel.send(message.channel, "listening", components=[
                    Button("listening", "hi there"),
                    SelectMenu("listening", options=[SelectOption(label="This is a option", value="my_value", description="This is the description of the option")]
                ]
            )


Slash-commands
====================


To create a new slash command, we need to acces the ``slash`` attribute from the initialized ``extension``


Basic command
~~~~~~~~~~~~~~

.. note::

    If you want to test slash commands, use ``guild_ids=["guild id to test herer"]``, because if you use global commands, 
    it will take some titme to create/update the slash command

In this example, we will create a simple slash command

.. code-block::

    @extension.slash.command(name="test", description="this is a test command", guild_ids=["785567635802816595"])
    async def command(ctx):
        ...

The command in discord would be

.. image:: images/slash/test_default.png
   :width: 1000

.. note::

    Replace ``785567635802816595`` with your guild id


Parameters
~~~~~~~~~~~~~~

To add parameters to the command, we change the code and use the ``options`` parameter

It acceps a list of :class:`~SlashOption`

.. code-block::

    @extension.slash.command(name="test", description="this is a test command", options=[
            SlashOption(int, name="parameter1", description="this is a parameter")
        ], guild_ids=["785567635802816595"])
    async def command(ctx, parameter1="nothing"):
        await ctx.respond("I got `" + str(parameter1) + "` for `parameter1`")


This will add a parameter that accepts a number to the slash command

.. image:: images/slash/test_param_optional.png
    :width: 1000

As you can see ``parameter1`` says "optional", which means you can use the command without to specify it

Because the parameter is optional, in the callback defenition, we have to set a default value for ``parameter``, which in this case is "nothing"

.. important::

    The name of the arguments the function accepts have to be the same as the argument name you specify in the discord slash command

Without the parameter

.. image:: images/slash/test_param_optional_usage_none.gif
    :width: 550

And with

.. image:: images/slash/test_param_optional_usage_1.gif
    :width: 550

As you can see, we said that the parameter only accepts integers (numbers), and when you try to use a string, it will say *Input a valid integer.*


If you want the parameter to be required, in the option, you have to set ``required`` to ``True``

.. code-block::

    @extension.slash.command(name="test", description="this is a test command", options=[
            SlashOption(int, name="parameter1", description="this is a parameter", required=True)
        ], guild_ids=["785567635802816595"])
    async def command(ctx, parameter1):
        await ctx.respond("I got `" + str(parameter1) + "` for `parameter1`")

.. image:: images/slash/test_param_options_required.gif
    :width: 550

.. note::

    the ``parameter`` argument of the callback function doesn't have a default value anymore, 
    because if the command is used, it will always get a value passed

Choices
~~~~~~~~~~

You can add choices for youur options, where the user can choose between a defined list of choices

Too add them, where we add the options with the :class:`~SlashOption` class, we use the ``choices`` parameter and change our code to


.. code-block::

    @extension.slash.command(name="test", description="this is a test command", options=[
                SlashOption(int, name="parameter1", description="this is a parameter", choices=[
                    {"name": "first choice", "value": 1}, {"name": "second choice", "value": 2}
                ])
            ], guild_ids=["785567635802816595"])
    async def command(ctx, parameter1="nothing"):
        await ctx.respond("I got `" + str(parameter1) + "` for `parameter1`")

Choices are a list of dict, where ``"name":`` is the displayed choice name and ``"value":`` is the real value, 
which will be received when the choice is selected 

.. image:: images/slash/test_param_choices.gif
    :width: 550

.. note::

    The value of the choice has to be of the same type then the option argument type, which in our case is ``int``, a number

Permissions
~~~~~~~~~~~~

You can set permissions for your commands
There are two ways to set permissions

default permission
--------------------

Default permissions apply to all servers, you can set them either to ``True`` or ``False``

If the default permission to ``False``, no one can use the command, if it's ``True``, everyone can use it


.. code-block::

    @extension.slash.command(name="test", description="this is a test command", options=[
            SlashOption(int, name="parameter1", description="this is a parameter")
        ], guild_ids=["785567635802816595"], default_permission=False)
    async def command(ctx, parameter1="nothing"):
        ...

In this example, no one can use the command


guild permissions
------------------

Additionallly, you can use guild permissions, which apply to guilds specified by guild ids

You can add role ids or/and user ids

.. code-block::

    @extension.slash.command(name="test", description="this is a test command", options=[
            SlashOption(int, name="parameter1", description="this is a parameter")
        ], guild_ids=["785567635802816595"], guild_permissions={
        "785567635802816595": SlashPermission(
            allowed_ids={ 
                "539459006847254542": SlashPermission.USER,
                "849035012476895232": SlashPermission.ROLE
            }, 
            forbidden_ids={ 
                "785567792899948577": SlashPermission.ROLE
            }
        )})
    async def command(ctx, parameter1="nothing"):
        ...

Allowed command

.. image:: images/slash/allowed_command.png
    :width: 1000

Forbidden command

.. image:: images/slash/forbidden_command.png
    :width: 1000


guild ids
~~~~~~~~~~~

You can decide if you want your commmand only be usable in some guilds you specify or globaly

To set the guilds where the command is useable, you need to set the ``guild_id`` parameter in the slash command to your list of guild ids

.. code-block::

    @extension.slash.command(name="test", description="this is a test command", guild_ids=["785567635802816595"])
    async def command(ctx, parameter1="nothing"):
        ...

Subcommands and Subcommandgroups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use subcommands and subcommand groups, they work almost the same as the normal slash command

subcommand
-----------

A subcommand is a slash command with the same base name that can have multiple subcommands

.. code-block::

    base
    |-- subcommand1
    |-- subcommand2

The only difference between ``subcommand`` and ``slashcommand`` is that you got a new ``base_name`` parameter.
This is the name of the parent command 

For example

.. code-block::

    @extension.slash.subcommand(base_name="hello", name="world", description="this is a subcommand")
    async def command(ctx):
        ...

would look like this

.. image:: images/slash/hello_world_subcommand.png
    :width: 1000

subcommand group
------------------
A subcommand group is a group of subucommands, you could see it like a subcommand of a subcommand


.. code-block::

    base
    |---subcommand
    |   |---subcommand
    |   |---subcommand
    |---subcommand
        |---subcommand

The difference between ``subcommand_group`` and ``subcommand`` is, that we got a new ``base_names`` parameter
They are the names of the parent commands

For example

.. code-block::

    @extension.slash.subcommand_group(base_names=["hello", "beautiful"], name="world", description="this is a subcommand group")
    async def command(ctx):
        ...

Would look like this

.. image:: images/slash/hello_beautiful_world_subcommandgroup.png
    :width: 1000