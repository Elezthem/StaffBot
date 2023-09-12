import disnake
from disnake.ext import commands

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!!", intents=intents)

class RecruitementModal1(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg  # arg - это аргумент, который передается в конструкторе класса RecruitementSelect
        components = [
            disnake.ui.TextInput(label="Your name and age", placeholder="Example: Vadim, 19", custom_id="name"),
            disnake.ui.TextInput(label="Your time zone", placeholder="Example: Moscow Time", custom_id="time"),
            disnake.ui.TextInput(label="Having experience in staff", placeholder="If so, how much?", custom_id="staff"),
            disnake.ui.TextInput(label="Tell me about yourself", placeholder="The more, the better!", custom_id="osebe")
        ]
        if self.arg == "helper":
            title = "Recruitment for the position of Assistant"
    
        super().__init__(title=title, components=components, custom_id="RecruitementModal1")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values["name"]
        time = interaction.text_values["time"]
        staff = interaction.text_values["staff"]
        osebe = interaction.text_values["osebe"]
        embed = disnake.Embed(color=0xfffff1, title="<a:yes:1068525712291663925>Application sent!\n")
        embed.description = f"> {interaction.author.mention}, Thank you for **applying**!\n" \
                            f"> If you are a **suitable** for us, the administration will **contact** you as soon as possible.\n\n" 
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        channel = interaction.guild.get_channel(1075833746160357416)  #  ID канала куда будут отправляться заявки
        await channel.send(f"**New application for** {self.arg} **from** {name} **|** {interaction.author.mention}\n\n**Time from Moscow time -** {time} \n\n**Staff info -** {staff}\n\n**About me -** {osebe}")


class RecruitementSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(emoji="<a:a_fire_vvns:1142805643858821180>",label="Assistant", value="helper", description="Following chats.")
        ]
        super().__init__(
            placeholder="Choose the desired role", options=options, min_values=0, max_values=1, custom_id="recruitement"
        )

    async def callback(self, interaction: disnake.MessageInteraction, timeout=None):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(RecruitementModal1(interaction.values[0]))


class Recruitement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command()
    async def recruit(self, ctx, timeout=None):
        view = disnake.ui.View()
        view.add_item(RecruitementSelect())
        helper = ctx.guild.get_role(1067827586534744115)
        embed = disnake.Embed(color=disnake.Colour.dark_purple())
        embed.set_author(name="Recruitment to the team of our server!\n")
        embed.description = f"<:blob_think:1113049818470809680> **What is required of you:**\n\n" \
                            "`1.` Knowledge of the **rules** of the server.\n" \
                            "`2.` Full `13` years.\n" \
                            "`3.` Stress resistance.\n" \
                            "`4.` **Possibility** to devote to the server from `2` hours per day.\n\n" \
                            "<a:adogdance:1113045393874370630> **What awaits you:**\n\n" \
                            "`1.` Opportunity to gain **valuable experience** and **career** growth.\n" \
                            "`2.` **Weekly** salary in the form of server currency, **Advertising your servers**, Drawings of **prizes**.\n\n" \
                            "<a:kirby_rave:1111578454413037608> **Branches:**\n" \
                            f"{helper.mention} — Responsible for **moderation of text** channels.\n\n"
        await ctx.send(embed=embed, view=view)
    

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitementSelect())
        self.bot.add_view(view,
                          message_id=(1109190479825875064))  # Вставить ID сообщения, которое отправится после использования с команда !recruit

@bot.event
async def on_ready():
    print("BOT connected")
    await bot.change_presence(
        status=disnake.Status.online,
        activity=disnake.Streaming(
            name="Набор в staff", url="https://www.twitch.tv/twitch"
        ),
    )


bot.add_cog(Recruitement(bot))

bot.run('token')