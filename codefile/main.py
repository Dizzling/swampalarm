import asyncio
import requests
from json import loads
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import os
from dotenv import load_dotenv

load_dotenv()
# 스프레드 시트 

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = 'key.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1-vdX3_wwAaKLGjlq6_YxUUDncLfozI1uaidulBC5xM4/edit?usp=sharing'
doc = gc.open_by_url(spreadsheet_url)
worksheet_words = doc.worksheet('알림글 설정')
worksheet_channel = doc.worksheet('알림 채널 설정')
worksheet_state = doc.worksheet('방송 현황')
worksheet_url = doc.worksheet('썸네일 url 설정')

# 트위치 API 
Url ='https://api.twitch.tv/helix/streams?user_login='
Url_profile = 'https://api.twitch.tv/helix/users?id='
AutURL ='https://id.twitch.tv/oauth2/token'

#트위치 api key
ClientId =os.getenv('CLIENTID')
Secret =os.getenv('SECRET')


# 디스코드 토큰
token = os.getenv('TOKEN')

# 트위치 ID, NAME 
twitch = ['jdm2088','kimnamsoon','nubulswamp','msmsms213','su_ning','esstree','95pingman','lita282','jungryeok']
name = ['악어','남봉','너불','멋사','수닝','만득','핑맨','리타','중력']

# 디스코드 봇
client = discord.Client()
while True: #api 요청 제한 오류 시, 계속해서 반복문을 실행하기 위함.
    try:
        @client.event
        async def on_ready():
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="  "))
            # 봇 초기 설정 ( 상태, 상태메세지 등 )

            AutParams = { 'client_id': ClientId, 'client_secret': Secret, 'grant_type': 'client_credentials'}
            AutCall = requests.post (url = AutURL, params = AutParams)
            data1 = AutCall.json()
            access_token = data1['access_token']
            Headers = {'Client-ID': ClientId, 'Authorization': "Bearer " + access_token}
            i=0
            
            while True:
                StreamsCall = requests.get(url=Url+twitch[i], headers=Headers)
                live_state = int(worksheet_state.acell('B'+str(i+2)).value)
                try:
                    if loads(StreamsCall.text)['data'][0]['type'] == 'live' and live_state == 0: 
                        #라이브 정보가 있고 && 방송 알림을 준 적이 있는지 체크
                        channel = client.get_channel(int(worksheet_channel.acell('B1').value)) #디스코드 알림을 줄 채널 설정
                        url_number = int(worksheet_url.acell('B'+str(i+2)).value) #썸네일 갱신 넘버 설정
                        url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{twitch[i]}-440x248.jpg={url_number}"#임베드 썸네일 주소
                        worksheet_url.update_acell('B'+str(i+2), str(int(url_number)+1)) #썸네일 갱신 후, number+=1 
                        alarm_word = worksheet_words.acell('B'+str(i+2)).value #각 멤버가 설정한 알람글 호출

                        #StreamsCall 정보 불러오기 및 저장 
                        gamename = loads(StreamsCall.text)['data'][0]['game_name'] 
                        title = loads(StreamsCall.text)['data'][0]['title']
                        userid = loads(StreamsCall.text)['data'][0]['user_id']
                        ProfilesCall = requests.get(url=Url_profile+userid, headers=Headers)
                        profiles_link = loads(ProfilesCall.text)['data'][0]['profile_image_url']

                        #임베드 설정 및 출력 
                        embed = discord.Embed(colour=discord.Colour.green(), title = f"{title}",url = f'https://www.twitch.tv/{twitch[i]}') #제목 출력 및 하이퍼링크
                        embed.set_author (name = f"{name[i]}", url = "https://twitter.com/RealDrewData", icon_url = profiles_link)
                        embed.add_field(name='Game',value=gamename,inline=False)
                        embed.set_image(url=url)
                        embed.set_footer (text = "제작 - @Tori1652 / 기능 추가 문의 및 버그 제보 - tori1652@naver.com")
                        #await channel.send(f"@everyone! {alarm_word} https://www.twitch.tv/{twitch[i]}", embed=embed) # embed와 메시지를 동시 출력.
                        await channel.send(f"{alarm_word} https://www.twitch.tv/{twitch[i]}", embed=embed) # embed와 메시지를 동시 출력.
                        worksheet_state.update_acell('B'+str(i+2), '1')
            
                except:
                    worksheet_state.update_acell('B'+str(i+2),'0') # 라이브 상태X  

                if i >= 8: #모든 리스트 확인 후 초기화
                    i = 0
                else :i+=1

                await asyncio.sleep(20)

        client.run(token) #디스코드 봇 토큰
    
    except BaseException:# 디스코드 봇 오프라인 예외처리
        print("client offline")

