import http.client
import json
import time
from fake_useragent import UserAgent

tokens = "tokens here"

print("""
░       █▀▀█ ─█▀▀█ ▀█▀ ░█▀▀▄ 　 ───░█ ░█▀▀▀█ ▀█▀ ░█▄─░█ ░█▀▀▀ ░█▀▀█ 
░       █▄▄▀ ░█▄▄█ ░█─ ░█─░█ 　 ─▄─░█ ░█──░█ ░█─ ░█░█░█ ░█▀▀▀ ░█▄▄▀ 
░       █─░█ ░█─░█ ▄█▄ ░█▄▄▀ 　 ░█▄▄█ ░█▄▄▄█ ▄█▄ ░█──▀█ ░█▄▄▄ ░█─░█
By Asura. any issues @asura, good luck :))
""")

class BloxEmpireJoiner:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            "Referer": "https://bloxempire.com/",
            "Authorization": tokens,
            "User-Agent": self.generate_useragent(),
            "Origin": "https://bloxempire.com",
            "Content-Type": "application/json"
        }
        self.conn = self.connection()

    def connection(self):
        return http.client.HTTPSConnection("api.bloxempire.com")

    def generate_useragent(self):
        return self.ua.random

    def request(self, method, endpoint):
        try:
            self.conn.request(method, endpoint, headers=self.headers)
            response = self.conn.getresponse()
            data = response.read().decode("utf-8")
            return response.status, data
        except Exception as e:
            print(e)
            self.conn = self.connection()
            return None, None

    def vailedtoken(self):
        status, data = self.request("GET", "/user/get-user")
        if status != 200:
            return None
        try:
            user_data = json.loads(data)
            if user_data.get('code') == 200:
                user_id = user_data['user']['id']
                print("Valid tokens :).\nAuto join start.")
                return user_id
            else:
                print("Invalid token.")
                return None
        except json.JSONDecodeError as e:
            print(e)
            return None

    def getinfo(self):
        status, response = self.request("GET", "/hourly/get-hourly-info")
        if status != 200:
            return None
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(e)
            return None

    def check(self, user_id, participants):
        for participant in participants:
            if participant['userId'] == user_id:
                return True
        return False

    def auto_join(self):
        user_id = self.vailedtoken()
        if user_id:
            while True:
                try:
                    info = self.getinfo()
                    if info is None:
                        time.sleep(5)
                        continue
                    participants = info.get('participants', [])
                    if not self.check(user_id, participants):
                        status, response = self.request("POST", "/hourly/join-hourly")
                        if status == 200:
                            print(f"Successfully joined  giveaway: {response}")
                        else:
                            print(f"Failed to join. retry in 5sec")
                    time.sleep(5)
                except Exception as e:
                    print(e)
                    time.sleep(5)

joiner = BloxEmpireJoiner()
joiner.auto_join()
