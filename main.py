from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
from nba_api.stats.static import players, teams
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents
from io import BytesIO
from PIL import Image
import pandas as pd
import requests
import discord
import json
import os

load_dotenv()
permissions = Intents.all()

acess_token = os.getenv('ACESS_TOKEN')
bot = commands.Bot(command_prefix='!', intents=permissions)

def altura_em_metros(altura_str):
    try:
        pes, polegadas = map(int, altura_str.split('-'))
        metros = (pes * 0.3048) + (polegadas * 0.0254)
        return round(metros, 2)
    except ValueError:
        return "Formato inválido. Use o formato 'PÉS-POLEGADAS', como '6-11'."
def peso_em_kg(peso_str):
    try:
        lbs = float(peso_str.strip())
        kg = lbs * 0.45359237
        return round(kg, 2)
    except ValueError:
        return "Formato inválido. Forneça o peso em libras como número. Ex: '220'"


@bot.event
async def on_ready():
    print(f'Running {bot.user.name} - {bot.user.id}')
    print('-=' * 20 + '-')
    
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def player(ctx: commands.Context):
    player_name = ctx.message.content.replace('!player ', '').strip()
    embed = discord.Embed(title=f"NBA Infos 🤓", color=discord.Color.red())
    try:
        player = players.find_players_by_full_name(player_name)
        if not player:
            await ctx.send(f"Jogador {player_name} não encontrado.")
            return
        
        player_id = player[0]["id"]
        player_data = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        infos = player_data.get_dict()
        common_info = infos['resultSets'][0]
        info_values = common_info['rowSet'][0]
        info_headers = common_info['headers']
        info_dict = dict(zip(info_headers, info_values))
        
        altura = altura_em_metros(info_dict['HEIGHT'])
        peso = peso_em_kg(info_dict['WEIGHT'])
        
        embed.add_field(name="Nome", value=info_dict['DISPLAY_FIRST_LAST'], inline=True)
        embed.add_field(name="Posição", value=info_dict['POSITION'], inline=True)
        embed.add_field(name="Time", value=f"{info_dict['TEAM_NAME']} ({info_dict['TEAM_ABBREVIATION']})", inline=True)
        embed.add_field(name="Altura", value=f"{altura} m", inline=True)
        embed.add_field(name="Peso", value=f"{peso} kg", inline=True)
        embed.add_field(name="Universidade", value=info_dict['SCHOOL'], inline=True)
        embed.add_field(name="Ano de Draft", value=info_dict['DRAFT_YEAR'], inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Rodada/Pick", value=f"{info_dict['DRAFT_ROUND']}ª / {info_dict['DRAFT_NUMBER']}º", inline=True)
        
        url_imagem = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
        response = requests.get(url_imagem)
        
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            image_file = discord.File(fp=image_bytes, filename="player.png")
            embed.set_image(url="attachment://player.png")
        else:
            await ctx.send(f"Imagem de {player_name} não encontrada.")
            
        stats = player_data.player_headline_stats.get_dict()
        status_json = stats['data'][0]
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="SEASON", value=f"{status_json[2]}", inline=False)
        embed.add_field(name="PTS", value=f"{status_json[3]}", inline=True)
        embed.add_field(name="AST", value=f"{status_json[4]}", inline=True)
        embed.add_field(name="REB", value=f"{status_json[5]}", inline=True)
        await ctx.send(embed=embed, file=image_file)
    except Exception as e:
        await ctx.send(f"Erro ao buscar dados de {player_name}.")
        print(e)
    
bot.run(acess_token)