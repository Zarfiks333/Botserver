import json
import random
import ast
from datetime import datetime
import os

import disnake

from disnake.ext import commands
from disnake.ext.commands import has_permissions

# These color constants are taken from discord.js library
with open("data/embed_colors.txt") as f:
    data = f.read()
    colors = ast.literal_eval(data)
    color_list = [c for c in colors.values()]

class Warn(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Define a new command
    @commands.command(
        name='warn',
        description='Знаменитая команда "warn"',
        usage='<@offender> called my mommy a fat :((((((( cri'
    )
    @has_permissions(administrator=True)
    async def warn_command(self, ctx, user:disnake.Member, *, reason:str):
        await ctx.message.delete()
        if user.id == self.bot.user.id:
            # User tried to warn this exact bot.
            await ctx.send("Нельзя предупредить Бота")
            return
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if not os.path.exists("data/warns/" + str(ctx.guild.id) + "/"):
            os.makedirs("data/warns/" + str(ctx.guild.id) + "/")
            # Checks if the folder for the guild exists. If it doesn't, create it.
        try:
            with open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json") as f:
                data = json.load(f)
            # See if the user has been warned
        except FileNotFoundError:
            # User has not been warned yet
            with open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json", "w") as f:
                data = ({
                    'offender_name':user.name,
                    'warns':1,
                    1:({
                        'warner':ctx.author.id,
                        'warner_name':ctx.author.name,
                        'reason':reason,
                        'channel':str(ctx.channel.id),
                        'datetime':dt_string
                    })
                }) # Creates the initial dictionary, which will then be dumped into a JSON file.
                json.dump(data, f)
            embed = disnake.Embed(
                title=f"Для {user.name}' выдан Warn",
                color=random.choice(color_list)
            )
            embed.set_author(
                name=ctx.message.author.name,
                url=f"https://discord.com/users/{ctx.message.author.id}/"
            )
            embed.add_field(
                name="Warn 1",
                value=f"Пользователь: {ctx.author.name} (<@{ctx.author.id}>)\nПричина: {reason}\nКанал: <#{str(ctx.channel.id)}>\nДата: {dt_string}",
                inline=True
            )
            await ctx.send(
                content=" Warn успешно выдан.",
                embed=embed
            )
            # Creates and sends embed, showing that the user has been warned successfully.
            return
            # using "return" so that it doesn't continue along the script

        # If the script made it this far, then the user has already been warned at least once.
        warn_amount = data.get("warns")
        new_warn_amount = warn_amount + 1
        data["warns"]=new_warn_amount
        data["offender_name"]=user.name
        new_warn = ({
            'warner':ctx.author.id,
            'warner_name':ctx.author.name,
            'reason':reason,
            'channel':str(ctx.channel.id),
            'datetime':dt_string
        })
        data[new_warn_amount]=new_warn
        json.dump(data, open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json", "a"))
        # Appends to dictionary, which will then be written inside the JSON.

        embed = disnake.Embed(
            title=f"Для {user.name}' выдан Warn",
            color=random.choice(color_list)
        )
        embed.set_author(
            name=ctx.message.author.name,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )
        embed.add_field(
            name=f"Warn {new_warn_amount}",
            value=f"Пользователь: {ctx.author.name} (<@{ctx.author.id}>)\nПричина: {reason}\nКанал: <#{str(ctx.channel.id)}>\nДата: {dt_string}",
            inline=True
        )
        await ctx.send(
            content="Warn Успешно выдан.",
            embed=embed
        )
        # Creates and sends embed
    @warn_command.error
    async def warn_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            # Author is missing permissions
            await ctx.send('{0.author.name}, у вас нет правильных разрешений для этого. '.format(ctx))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                # Author did not specify the user to warn
                await ctx.send("{0.author.name}, вы забыли указать пользователя для предупреждения. ".format(ctx))
                return
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'reason':
                # Author did not specify the reason
                await ctx.send("{0.author.name}, Вы забыли указать причину.".format(ctx))
                return
        print(error)
        await ctx.send(error)

    @commands.command(
        name='warns',
        description='Просмотреть все предупреждения, которые есть у пользователя',
        usage='<@offender>',
        aliases=['warnings','warnl',"warnlist"]
    )
    async def warns_command(self, ctx, user:disnake.Member):
        await ctx.message.delete()
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
            # See if the user has been warned
        except FileNotFoundError:
            # User does not have any warns.
            await ctx.send(f"{ctx.author.name}, пользователь [{user.name} ({user.id})] не имеет никаких предупреждений.")
            return


        warn_amount = data.get("warns")
        last_noted_name = data.get("offender_name")
        if warn_amount == 1:
            warns_word = "warn"
        else:
            warns_word = "warns"


        try:
            username = user.name
        except:

            username = last_noted_name


        embed = disnake.Embed(
            title=f"{username}",
            description=f"есть {warn_amount} {warns_word}.",
            color=random.choice(color_list)
        )
        embed.set_author(
            name=ctx.message.author.name,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )
        for x in range (1,warn_amount+1):
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)

            warn_dict = data.get(str(x))
            warner_id = warn_dict.get('warner')
            try:
                warner_name = self.bot.get_user(id=warner_id)
            except:
                # User probably left
                warner_name = warn_dict.get('warner_name')

            warn_reason = warn_dict.get('reason')
            warn_channel = warn_dict.get('channel')
            warn_datetime = warn_dict.get('datetime')

            embed.add_field(
                name=f"Warn {x}",
                value=f"Пользователь: {warner_name} (<@{warner_id}>)\nПричина: {warn_reason}\nКанал: <#{warn_channel}>\nДата и время: {warn_datetime}",
                inline=True
            )
            # For every warn between 1 and warn_amount+1, get the info of that warn and put it inside an embed field.
        await ctx.send(
            content=None,
            embed=embed
        )
        # Send embed.
    @warns_command.error
    async def warns_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                await ctx.send("Пожалуйста, упомяните кого-нибудь, чтобы подтвердить варн.")
                return
        await ctx.send(error)

    @commands.command(
        name='remove_warn',
        description='Удаляет конкретное предупреждение от конкретного пользователя.',
        usage='@user 2',
        aliases=['removewarn','clearwarn','rwarn','cwarn']
    )
    @has_permissions(administrator=True)
    async def remove_warn_command(self, ctx, user:disnake.Member, *, warn:str):
        await ctx.message.delete()
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
            # See if the user has been warned
        except FileNotFoundError:
            # User does not have any warns.
            await ctx.send(f"[{ctx.author.name}], пользователь [{user.name} ({user.id})] не имеет никаких предупреждений.")
            return
        warn_amount = data.get('warns')
        specified_warn = data.get(warn)
        warn_warner = specified_warn.get('warner')
        warn_reason = specified_warn.get('reason')
        warn_channel = specified_warn.get('channel')
        warn_datetime = specified_warn.get('datetime')
        try:
            warn_warner_name = self.bot.get_user(id=warn_warner)
        except:
            # User probably left
            warn_warner_name = specified_warn.get('warner_name')

        confirmation_embed = disnake.Embed(
            title=f'{user.name}\'  номер warn {warn}',
            description=f'Пользователь: {warn_warner_name}\nПричина: {warn_reason}\nКанал: <#{warn_channel}>\nДата: {warn_datetime}',
            color=random.choice(color_list),
        )
        confirmation_embed.set_author(
            name=ctx.message.author.name,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )
        def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send(content='Вы уверены, что хотите это сделать? (Ответьте y/да или n/нет)', embed=confirmation_embed)
        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.lower() # Set the reply into a string
        if reply in ('y', 'yes', 'confirm'):
            # do the whole removing process.
            if warn_amount == 1: # Check if the user only has one warn.
                os.remove("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json") # Removes the JSON containing their only warn.
                await ctx.send(f"[{ctx.author.name}], Пользователь [{user.name} ({user.id})] было удалено предупреждение.")
                return
            # User does not have only one warn.
            if warn != warn_amount: # Check if the warn to remove was not the last warn.
                for x in range(int(warn),int(warn_amount)):
                    data[str(x)] = data[str(x+1)]
                    del data[str(x+1)]
                    # Puts all warns with a value higher than the current specified warn back by one (I suck at explaining)
            else:
                del data[warn]
                # It was their last warn.
            data['warns']=warn_amount - 1
            json.dump(data,open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "w"))
            await ctx.send(f"[{ctx.author.name}], Пользователь [{user.name} ({user.id})] было удалено предупреждение.")
            return
        elif reply in ('n', 'no', 'cancel'):
            await ctx.send("Хорошо, aks отменена.")
            return
        else:
            await ctx.send("Я понятия не имею, чего ты от меня хочешь. aks отменена.")
    @remove_warn_command.error
    async def remove_warn_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                # Author did not specify a user
                await ctx.send("Пожалуйста, упомяните кого-нибудь, чтобы удалить их предупреждения.")
                return
            if error.param.name == 'warn':
                # Author did not specify a warn ID
                await ctx.send("Вы не указали идентификатор предупреждения для удаления.")
                return
        if isinstance(error, commands.CommandInvokeError):
            # Author probably specified an invalid ID.
            await ctx.send("Вы указали недопустимый идентификатор.")
            return
        await ctx.send(error)

    @commands.command(
        name='edit_warn',
        description='Редактирует конкретное предупреждение от конкретного пользователя.',
        usage='@user 2',
        aliases=['editwarn','changewarn']
    )
    @has_permissions(administrator=True)
    async def edit_warn_command(self, ctx, user:disnake.Member, *, warn:str):
        await ctx.message.delete()
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
            # See if the user has been warned
        except FileNotFoundError:
            # User does not have any warns.
            await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] does not have any warns.")
            return


        def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send(content='Какую бы вы хотели причину warn \' изменить на ?')
        msg = await self.bot.wait_for('message', check=check) # Pause the ongoing script to wait for the user to send a message.
        warn_new_reason = msg.content.lower()

        specified_warn = data.get(warn)
        warn_warner = specified_warn.get('warner')
        warn_channel = specified_warn.get('channel')
        warn_datetime = specified_warn.get('datetime')
        try:
            warn_warner_name = self.bot.get_user(id=warn_warner)
        except:
            # User probably left
            warn_warner_name = specified_warn.get('warner_name')

        confirmation_embed = disnake.Embed(
            title=f'{user.name}\'  номер warn {warn}',
            description=f'Пользователь: {warn_warner_name}\nПричина: {warn_new_reason}\nКанал: <#{warn_channel}>\nДата: {warn_datetime}',
            color=random.choice(color_list),
        )
        confirmation_embed.set_author(
            name=ctx.message.author.name,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )

        await ctx.send(content='Вы уверены, что хотите это сделать? (Ответьте y/да или n/нет)', embed=confirmation_embed)

        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.lower() # Set the title
        if reply in ('y', 'yes', 'confirm'):
            specified_warn['reason']=warn_new_reason
            json.dump(data,open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "w"))
            await ctx.send(f"[{ctx.author.name}], Пользователь [{user.name} ({user.id})] отредактировал их предупреждение.")
            return
        elif reply in ('n', 'no', 'cancel', 'flanksteak'):
            # dont ask me why i decided to put flanksteak
            await ctx.send("Хорошо, ask отменён.")
            return
        else:
            await ctx.send("Я понятия не имею, чего ты от меня хочешь. Акция отменена.")
    @edit_warn_command.error
    async def edit_warn_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                # Author did not specify a user
                await ctx.send("Пожалуйста, упомяните кого-нибудь, чтобы удалить их предупреждения.")
                return
            if error.param.name == 'warn':
                # Author did not specify a warn ID
                await ctx.send("Вы не указали идентификатор предупреждения для удаления.")
                return
        if isinstance(error, commands.CommandInvokeError):
            # Author probably specified an invalid ID.
            await ctx.send("Вы указали недопустимый идентификатор.")
            return
        await ctx.send(error)

def setup(bot):
    bot.add_cog(Warn(bot))
