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
async def poll(client: discord.Client, message: discord.Message, *):
    help_embed = discord.Embed(title="Poll-Commands of the Belissibot", colour=discord.Color(0xFFFF00),
                          description="Tip: Add a `help` to any command to show its help.")
    help_embed.add_field(name="`!poll new`", value="Creates a new poll.", inline=False)
    help_embed.add_field(name="`!poll add <answer>`", value="Adds a choice to your poll.", inline=False)
    help_embed.add_field(name="`!poll remove <number>`", value="Removes the specified choice from your poll.", inline=False)
    help_embed.add_field(name="`!poll publish`", value="Makes the poll uneditable and sets up the reactions.", inline=False)
    
    await message.channel.send(embed=help_embed)


@app.route("!poll new", raw_args=True)
async def poll(client: discord.Client, message: discord.Message, question):
    embed = discord.Embed(title="Frage: " + question, colour=discord.Color(0x7100aa),
                          description=description_factory([]))
    embed.set_footer(text="__________________________________________________\n"
                          "-> to remove a add type !poll remove <number>.\n"
                          "-> to publish the poll type !poll publish.")
    message_of_user_id_dict[message.author.id] = (await message.channel.send(embed=embed)).id, []
    await message.delete()

@app.route("!poll add", raw_args=True)
async def poll(client: discord.Client, message: discord.Message, choice):
    pollmessage_id, choices = message_of_user_id_dict[message.author.id]
    pollmessage = await message.channel.fetch_message(pollmessage_id)
    if len(choices) >= 9:
        return
    choices.append(choice)
    embed = pollmessage.embeds[0]
    embed.description = description_factory(choices)
    await pollmessage.edit(embed=embed)
    await message.delete()


@app.route("!poll remove", raw_args=True)
async def poll(client: discord.Client, message: discord.Message, number):
    pollmessage_id, choices = message_of_user_id_dict[message.author.id]
    pollmessage = await message.channel.fetch_message(pollmessage_id)
    del choices[int(number) - 1]
    embed = pollmessage.embeds[0]
    embed.description = description_factory(choices)
    await pollmessage.edit(embed=embed)
    await message.delete()


@app.route("!poll publish")
async def poll(client: discord.Client, message: discord.Message):
    pollmessage_id, choices = message_of_user_id_dict[message.author.id]
    pollmessage = await message.channel.fetch_message(pollmessage_id)
    # react with choicenumbers
    for index in range(len(choices)):
        await pollmessage.add_reaction(emoji_factory(index + 1))
    # delete relation from message of user id
    del message_of_user_id_dict[message.author.id]
    await message.delete()


def description_factory(choices: list[str]):
    out = ""
    for index, line in enumerate(choices):
        out += "\n" + emoji_factory(index + 1) + f"`{line}`"
    if len(choices) >= 9:
        out += "\n\n_maximum number of answers reached_"
    else:
        out += "\n\n_add a new option to answer by typing !poll add <your answer>_"
    return out


def emoji_factory(number):
    return str(number) + b"\xef\xb8\x8f\xe2\x83\xa3".decode()


with open("secret.token", "r") as f:
    TOKEN = f.read()

app.run(discord_token=TOKEN)
