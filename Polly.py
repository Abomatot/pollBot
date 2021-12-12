import discord as discord
from belissibot_framework import App

message_of_user_id_dict = {}
app = App()


@app.route("!belissibot")
async def belissibot_help(client: discord.Client, message: discord.Message):
    help_embed = discord.Embed(title="Commands of the Belissibot", color=discord.Color(0xFFFF00))
    help_embed.add_field(name="`!poll`", value="Shows all commands related to the poll-functionality.",
                         inline=False)

    await message.channel.send(embed=help_embed)


@app.route("!poll", raw_args=True)
async def poll(client: discord.Client, message: discord.Message, _=""):
    help_embed = discord.Embed(title="Poll-Commands of the Belissibot", colour=discord.Color(0xFFFF00),
                               description="Tip: Add a `help` to any command to show its help.")
    help_embed.add_field(name="`!poll new`", value="Creates a new poll.", inline=False)
    help_embed.add_field(name="`!poll choice <choice>`", value="Adds a choice to your poll.", inline=False)
    help_embed.add_field(name="`!poll remove <choice number>`", value="Removes the specified choice from your poll.",
                         inline=False)
    help_embed.add_field(name="`!poll publish`", value="Makes the poll uneditable and sets up the reactions.",
                         inline=False)

    await message.channel.send(embed=help_embed)


@app.route("!poll new", raw_args=True)
async def new(client: discord.Client, message: discord.Message, question):
    embed = discord.Embed(title="Frage: " + question, colour=discord.Color(0xff7fff),
                          description=description_factory([]))
    embed.set_footer(text="-> to remove a choice, type !poll remove <choice number>.\n"
                          "-> to publish the poll, type !poll publish.")
    message_of_user_id_dict[message.author.id] = (await message.channel.send(embed=embed)).id, []


@app.route("!poll new help")
async def new_help(client: discord.Client, message: discord.Message):
    help_embed = discord.Embed(title="Usage of `!poll new`",
                               description="Usage: `!poll new <question>`\n\nExample: "
                                           "```!poll new Welche Farbe haben Elefanten?```",
                               color=discord.Color(0xFFFF00))

    help_embed.add_field(name="question", value="The question to initiate a new poll with.")

    await message.channel.send(embed=help_embed)


@app.route("!poll choice", raw_args=True)
async def add(client: discord.Client, message: discord.Message, choice):
    pollmessage_id, choices = message_of_user_id_dict[message.author.id]
    pollmessage = await message.channel.fetch_message(pollmessage_id)
    if len(choices) >= 9:
        return
    choices.append(choice)
    embed = pollmessage.embeds[0]
    embed.description = description_factory(choices)
    await pollmessage.edit(embed=embed)


@app.route("!poll choice help")
async def add_help(client: discord.Client, message: discord.Message):
    help_embed = discord.Embed(title="Usage of `!poll choice`",
                               description="Usage: `!poll choice <choice>`\n\nExample: ```!poll choice lila```",
                               color=discord.Color(0xFFFF00))

    help_embed.add_field(name="choice", value="The choice to add to the current poll.")

    await message.channel.send(embed=help_embed)


@app.route("!poll remove", raw_args=True)
async def remove(client: discord.Client, message: discord.Message, number):
    pollmessage_id, choices = message_of_user_id_dict[message.author.id]
    pollmessage = await message.channel.fetch_message(pollmessage_id)
    del choices[int(number) - 1]
    embed = pollmessage.embeds[0]
    embed.description = description_factory(choices)
    await pollmessage.edit(embed=embed)


@app.route("!poll remove help")
async def remove_help(client: discord.Client, message: discord.Message):
    help_embed = discord.Embed(title="Usage of `!poll remove`",
                               description="Usage: `!poll remove <choice number>`\n\nExample: ```!poll remove 1```",
                               color=discord.Color(0xFFFF00))

    help_embed.add_field(name="choice number", value="The number of the choice to remove from the current poll.")

    await message.channel.send(embed=help_embed)


@app.route("!poll publish")
async def publish(client: discord.Client, message: discord.Message):
    pollmessage_id, choices = message_of_user_id_dict[message.author.id]
    pollmessage = await message.channel.fetch_message(pollmessage_id)

    # react with choicenumbers
    for index in range(len(choices)):
        await pollmessage.add_reaction(emoji_factory(index + 1))

    # remove help messages
    embed: discord.Embed = pollmessage.embeds[0]
    embed.description = description_factory(choices, remove_help=True)
    embed.colour = discord.Color(0x7100aa)
    embed.set_footer()
    await pollmessage.edit(embed=embed)

    # delete relation from message of user id
    del message_of_user_id_dict[message.author.id]


@app.route("!poll publish help")
async def publish_help(client: discord.Client, message: discord.Message):
    help_embed = discord.Embed(title="Usage of `!poll publish`",
                               description="Usage: `!poll publish`\n\nExample: ```!poll publish```",
                               color=discord.Color(0xFFFF00))

    await message.channel.send(embed=help_embed)


def description_factory(choices: list[str], remove_help=False):
    out = ""
    for index, line in enumerate(choices):
        out += "\n" + emoji_factory(index + 1) + f" `{line}`"

    if remove_help:
        return out

    if len(choices) >= 9:
        out += "\n\n_maximum number of answers reached_"
    else:
        out += "\n\n_add a new choice by typing !poll choice <choice>_"
    return out


def emoji_factory(number):
    return str(number) + b"\xef\xb8\x8f\xe2\x83\xa3".decode()


with open("secret.token", "r") as f:
    TOKEN = f.read()

app.run(discord_token=TOKEN)
