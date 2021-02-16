from discord import channel, state
import requests
from json import loads
import discord
from discord.ext import commands
import os

client =  discord.Client()

Url ='https://api.twitch.tv/helix/streams?user_login='
AutURL ='https://id.twitch.tv/oauth2/token'
ClientId ='9d9ndlpo5bvv7tek1yodf5p6uyk5lr'
Secret ='8rc9b6r8orj9wfnw0mn9y7nbkbcm7l'

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game('test')
    await client.change_presence(status=discord.Status.online,activity=game)
    AutParams = { 'client_id': ClientId, 'client_secret': Secret, 'grant_type': 'client_credentials'}
    AutCall = requests.post (url = AutURL, params = AutParams)

    data1 = AutCall.json()
    access_token = data1['access_token']
    Headers = {'Client-ID': ClientId, 'Authorization': "Bearer " + access_token}
    channel = client.get_channel(808879011417423892)
    twitch = ['jdm2088','kimnamsoon','nubulswamp','msmsms213','su_ning','esstree','95pingman','lita282','jungryeok']
    name = ['악어','남봉','너불','멋사','수닝','만득','핑맨','리타','중력']
    a = [0,0,0,0,0,0,0,0,0] #방송중 1 , 방송 X 0
    i=0

    while True:
        StreamsCall = requests.get(url=Url+twitch[i], headers=Headers)
        try:
            if loads(StreamsCall.text)['data'][0]['type'] == 'live' and a[i] == 0: #라이브 정보가 위치하는 곳 
                await channel.send("@everyone")
                embed = discord.Embed(colour=discord.Colour.green(), title = "《 늪지대 생방송 알림 》")
                #await channel.send("@everyone"+name[i] + "님이 방송 중입니다")
                embed.add_field(name=f'{name[i]}님이 방송중입니다',value=f'https://www.twitch.tv/{twitch[i]} 에서 시청하세요',inline=False)
                await channel.send(embed=embed)
                a[i]=1

        except:
            a[i] = 0

        if i >= 8: #모든 리스트 확인 후 초기화
            i = 0
        else :i+=1

access_token = os.environ['BOT_TOKEN']
client.run(token)
