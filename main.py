import asyncio
import datetime

import disnake
from config import settings
import json
from disnake.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=disnake.Intents().all())

bot.remove_command('help')

cogs = ['cogs.warn']




@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Game(name="АндЧилл"))
    print("Started")
    for cog in cogs:
            bot.load_extension(cog)
            # Loads every cog provided.
    return
#БАН

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: disnake.Member, reason=None):
        await ctx.message.delete()
        await member.ban(reason=reason)
        times_start = datetime.datetime.today()

        emb_user = disnake.Embed(title='**Уведомление - Ban**', color=0xd36969)
        emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
        emb_user.add_field(name='**Причина:**', value=reason, inline=False)
        emb_user.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
        emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        emb_user.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

        logs = bot.get_channel(1055172314519580723);
        embed=disnake.Embed(title=f"Пользователь {member.name} был забанен.", description=f"Причина блокировки: {reason}", color=0xd36969)
        embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/5426/5426867.png')
        embed.set_footer(text=f"Выполнено " + ctx.author.name +"#"+ ctx.author.discriminator, icon_url=ctx.author.avatar.url)
        await member.send(embed=embed)
        await ctx.send(embed=embed)
        logembed=disnake.Embed(title=f"Пользователь {member.name} был забанен.", description=f"Указанная причина блокировки: {reason}", color=0x0B729D)
        logembed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/5426/5426867.png')
        logembed.set_footer(text=f"Выполнено " + ctx.author.name +"#"+ ctx.author.discriminator, icon_url=ctx.author.avatar.url)
        await logs.send(embed=logembed)
        await member.send(embed=emb_user)
        AddBan()

#разбан

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, * ,member : disnake.Member):
    await ctx.message.delete()
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            logs = bot.get_channel(955057757214621727);  # вставляем айди канала с логами
            logembed = disnake.Embed(description=f"Пользователь {member.name} был разбанен", color=0x0B729D)
            logembed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/5426/5426867.png')
            logembed.set_footer(text=f"Выполнено " + ctx.author.name + "#" + ctx.author.discriminator,icon_url=ctx.author.avatar.url)

            await logs.send(embed=logembed)  # отправляем эмбед в логи
            return

#кик

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: disnake.Member):
    await ctx.message.delete()
    await member.kick(member)

    times_start = datetime.datetime.today()
    emb_user_stop = disnake.Embed(title='**Кик**', color=0xd36969)
    emb_user_stop.add_field(name='**Кикнут Поьзователем:**', value=ctx.author.mention, inline=False)
    emb_user_stop.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
    emb_user_stop.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
    emb_user_stop.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

    logs = bot.get_channel(955057757214621727);  # вставляем айди канала с логами
    logembed = disnake.Embed(description=f"Пользователь {member.name} был кикнут", color=0x0B729D)
    logembed.set_thumbnail(url='https://www.clipartkey.com/mpngs/m/307-3078950_expulsion-icon.png')
    logembed.set_footer(text=f"Выполнено " + ctx.author.name + "#" + ctx.author.discriminator,icon_url=ctx.author.avatar.url)
    await logs.send(embed=logembed)  # отправляем эмбед в логи
    await member.send(embed=emb_user_stop)

#очистка

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True) # проверка на права администрирования сервером
async def clear(ctx, limit: int): # задаем параметр команды limit который является целым числом


        logs = bot.get_channel(955057757214621727); # вставляем айди канала с логами
        channel = ctx.message.channel # определяем канал для удаления сообщений (там где была отправлена команда)
        await ctx.message.delete() # удаляем сообщение содержащее команду
        await ctx.channel.purge(limit=limit) # очищаем limit последних сообщений
        logembed=disnake.Embed(title=f"В чате {channel} удалено {limit} сообщений.", color=0x0B729D) # тот же эмбед только в логи.
        logembed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/5181/5181185.png')
        logembed.set_footer(text=f"Выполнено " + ctx.author.name +"#"+ ctx.author.discriminator, icon_url=ctx.author.avatar.url)
        await logs.send(embed=logembed) # отправляем эмбед в логи


#mute

@bot.command(aliases=['Mute'])
@commands.has_permissions(administrator=True)
async def mute(ctx, member: disnake.Member = None, amout: str = None, *, reason=None):
    await ctx.message.delete()
    times_start = datetime.datetime.today()

    emb_user = disnake.Embed(title='**Уведомление - Mute**', color=0xd36969)
    emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
    emb_user.add_field(name='**Причина:**', value=reason, inline=False)
    emb_user.add_field(name='**Длительность:**', value=amout, inline=False)
    emb_user.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
    emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')


    emb_user_stop = disnake.Embed(title='**Уведомление - Unmute**', color=0xd36969)
    emb_user_stop.add_field(name='**Снял:**', value=ctx.author.mention, inline=False)
    emb_user_stop.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
    emb_user_stop.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
    mute_role = disnake.utils.get(ctx.message.guild.roles, id=736195143811596348)


    if member is None:
        emb = disnake.Embed(title='[ERROR] Mute', description=f'{ctx.author.mention}, Укажите пользователя!', color=0xd36969)
        emb.add_field(name='Пример:', value=f'{ctx.prefix}mute пользователь время(с, м, ч, д) причина', inline=False)
        emb.add_field(name='Пример 1:', value=f'{ctx.prefix}mute @Use 1ч пример')
        emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')
        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

        await ctx.send(embed=emb)
    else:
        end_time = amout[-1:]
        time = int(amout[:-1])
        if time <= 0:
            emb = disnake.Embed(title='[ERROR] Mute',description=f'{ctx.author.mention}, Время не может быть меньше 1!', color=0xd36969)
            emb.add_field(name='Пример:', value=f'{ctx.prefix}mute пользователь время причина', inline=False)
            emb.add_field(name='Пример 1:', value=f'{ctx.prefix}mute @User 1ч пример')
            emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')
            emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

            await ctx.send(embed=emb)
        else:
            if end_time == 'с':
                if reason is None:
                    emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value='Не указано', inline=False)
                    emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
                else:
                    emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value=reason, inline=False)
                    emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
            elif end_time == 'м':
                if reason is None:
                    emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value='Не указано', inline=False)
                    emb.add_field(name='Длительность:', value='{} минут'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
                else:
                    emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                    emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                    emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                    emb.add_field(name='Причина:', value=reason, inline=False)
                    emb.add_field(name='Длительность:', value='{} минут'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                    emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
            elif end_time == 'ч':
                if reason is None:
                    if time == '1':

                        emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} час'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    elif time == '4' or time == '3' or time == '2':
                        emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    elif time >= '5':
                        emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                        emb.add_field(name='**Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='**Причина:', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:', value='{} часов'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)

                else:
                    if time == '1':
                        emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} час'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)

                    elif time == '4' or time == '3' or time == '2':
                        emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} часа'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    elif time >= '5':
                        emb = disnake.Embed(title=f'**Mute**', color=0xd36969)
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")

                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
            elif time == 'д':
                if reason is None:
                    emb = disnake.Embed(title=f'**System - Mute**', color=0xd36969)
                    emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                    emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                    emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                    emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                    emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time))
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')


                    await member.send(embed=emb_user)
                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60 * 60 * 24)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)
                else:
                    emb = disnake.Embed(title=f'**System - Mute**', color=0xd36969)
                    emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                    emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                    emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                    emb.add_field(name='**Причина:**', value=reason, inline=False)
                    emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time), inline=False)
                    emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                    await member.add_roles(mute_role)
                    await ctx.send(embed=emb)
                    await member.send(embed=emb_user)
                    await asyncio.sleep(time * 60 * 60 * 24)
                    await member.remove_roles(mute_role)
                    await member.send(embed=emb_user_stop)


@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: disnake.Member=None):
    await ctx.message.delete()

    times_start = datetime.datetime.today()
    emb_user_stop = disnake.Embed(title='**Уведомление - Unmute**', color=0xd36969)
    emb_user_stop.add_field(name='**Снял:**', value=ctx.author.mention, inline=False)
    emb_user_stop.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
    emb_user_stop.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
    emb_user_stop.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
    role = disnake.utils.get(ctx.message.guild.roles, id=736195143811596348)

    if member is None:
        emb = disnake.Embed(title='UNMUTE', description=f'{ctx.author.mention}, Укажите пользователя!', color=0xd36969)
        emb.add_field(name='Пример:', value=f'{ctx.prefix}unmute пользователь ', inline=False)
        emb.add_field(name='Пример 1:', value=f'{ctx.prefix}unmute @User  ')
        emb.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
        await ctx.send(embed=emb)
    else:
        await member.remove_roles(role)
        await member.send(embed=emb_user_stop)


#новый участник

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(955034723598598214) # вместо idservera - айди вашего сервера (ПКМ на сервер в списке, Копировать айди)
    priwet = bot.get_channel (955048769932623872)
    role = disnake.utils.get(guild.roles, name="название роли")
    newinke = disnake.Embed(title=f"Унас Новичёк {member.name} Удачки тебе освоить новый мир.", description=f"",color=0xd36269)
    await member.add_roles(role)
    await priwet.send(embed=newinke)

#рольки по реакции

@bot.event
async def on_raw_reaction_add(payload):
    ourMessageID = 1075786554305433630 # айди сообщения (сначала создаем его командой !react, а потом копируем его айди и вписываем сюда)

    if ourMessageID == payload.message_id:
        member = payload.member # определяем юзера
        guild = member.guild # определяем сервер

        emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
        if emoji == '🤓': # само эмоджи
            role = disnake.utils.get(guild.roles, id=1066033182690005012) # определяем роль которую будем выдавать
            await member.add_roles(role) # выдаем рольку

    if ourMessageID == payload.message_id:
        member = payload.member # определяем юзера
        guild = member.guild # определяем сервер

        emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
        if emoji == '😛': # само эмоджи
            role = disnake.utils.get(guild.roles, id=1066033235613716532 ) # определяем роль которую будем выдавать
            await member.add_roles(role) # выдаем рольку


@bot.event
async def on_raw_reaction_remove(payload):
    ourMessageID = 1075786554305433630 # айди сообщения (сначала создаем его командой !react, а потом копируем его айди и вписываем сюда)

    if ourMessageID == payload.message_id:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
        if emoji == '🤓': # само эмоджи
            role = disnake.utils.get(guild.roles, id = 1066033182690005012 ) # определяем роль которую будем выдавать

            member = await(guild.fetch_member(payload.user_id))
            if member is not None: # проверяем есть ли он на сервере
                await member.remove_roles(role) # забираем рольку
            else:
                print('not found')

    if ourMessageID == payload.message_id:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name # эмоджи при нажатии на которое выдается роль
        if emoji == '😛': # само эмоджи
            role = disnake.utils.get(guild.roles, id = 1066033235613716532) # определяем роль которую будем выдавать

            member = await(guild.fetch_member(payload.user_id))
            if member is not None: # проверяем есть ли он на сервере
                await member.remove_roles(role) # забираем рольку
            else:
                print('not found')



@bot.command()
async def react(ctx):
    channel = bot.get_channel(1066048517501632522) # определяем канал, куда будет отправлено сообщение с эмбедом и реакциями
    embed=disnake.Embed(title="Бери рольки", description="""роли""", color=0x5e7abd) # сам эмбед
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1545/1545324.png") # кортиночка
    mojj = await channel.send(embed=embed)
    await mojj.add_reaction('🤓')
    await mojj.add_reaction('😛')
    await mojj.add_reaction('🤣')
    await mojj.add_reaction('😍')# отправляем эмбед + добавляем реакцию

#добавка баннов

def AddBan():
    with open('bd.json', 'r') as f:
        json_data = json.load(f)
        json_data['bans'] += 1 # добавляем 1 к числу
    with open('bd.json', 'w') as f:
        f.write(json.dumps(json_data)) # записываем данные


#выдача ролей

@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def giverole(ctx , user: disnake.Member, *, role: disnake.Role):
    await ctx.message.delete()
    await user.add_roles(role)
    embed = disnake.Embed(title=f"Заявка на сервер АндЧилл",description=f"Приветствую, твоя заявка\n на сервер АндЧилл была одобрена \nДальнейшую информацию ты можешь получить тут: ",color=0xd36969)
    embed.add_field(name="",value=ctx.author.mention, inline=False)
    embed.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
    embed.add_field(name="Discord",value="https://discord.gg/DNvE6b2q")
    await user.send(embed=embed)

#cogs

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#help

@bot.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
    await ctx.message.delete()
    emb1 = disnake.Embed(title="Доступные команды:",description=f"🛡️ Модерирование (!helpmod)\n👑 Роли (!helprole)\n", color=0xd36969)
    emb1.add_field(name = "!help : ", value="Вызовет это меню", inline=False)
    emb1.add_field(name="!helpmod : ", value="Вызовет меню комманд 🛡️ Модерирование ", inline=False)
    emb1.add_field(name="!helprole : ", value="Вызовет меню комманд 👑 Роли ", inline=False)
    emb1.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
    await ctx.send(embed = emb1)

@bot.command(pass_context = True)
async def helpmod(ctx):
    emb1 = disnake.Embed(title="Доступные команды:",description=f"🛡️  Модерирование ", color=0xd36969)
    emb1.add_field(name="!ban : ", value="Заблакировать участника на сервере\n(!ban пользователь причина)", inline=False)
    emb1.add_field(name="!unban : ", value="Разбан\n(!unban пользователь)", inline=False)
    emb1.add_field(name="!kick : ", value="Выгнать участника на сервере\n(!kick пользователь)", inline=False)
    emb1.add_field(name="!mute : ", value="Замутить пользователя\n(!mute пользователь время с/м/ч/д )",inline=False)
    emb1.add_field(name="!clear : ", value="Очистка чата\n(!clear количество)", inline=False)
    emb1.add_field(name="!warn : ", value="Предупреждение\n(!warn пользователь причина)", inline=False)
    emb1.add_field(name="!cwarn,!rwarn : ", value="Снять предупреждение\n(!cwarn пользователь причина)", inline=False)
    emb1.add_field(name="!warnl : ", value="Посмотреть предупреждение пользователя\n(!warnl пользователь )", inline=False)
    emb1.add_field(name="!editwarn : ", value="Редактировать предупреждение\n(!editwarn пользователь причина)", inline=False)
    emb1.set_thumbnail(url="https://wmpics.space/di-A1EN.png")
    await ctx.send(embed=emb1)


bot.run(settings["token"])
