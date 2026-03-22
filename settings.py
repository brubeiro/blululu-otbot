import configparser
import os

class Settings:
    def __init__(self, filename='config.ini'):
        self.filename = filename
        self.address = {}
        self.config = configparser.ConfigParser()
        self.all_servers = []
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.filename):
            print(f"Erro: Arquivo {self.filename} não encontrado!")
            return
        self.config.read(self.filename)
        self.all_servers = self.config.sections()
        if self.all_servers:
            self.set_server(self.all_servers[0])

    def set_server(self, server_name):
        if server_name in self.config:
            self.address = {}
            for key, value in self.config[server_name].items():
                if isinstance(value, str) and '&H' in value.upper():
                    try:
                        clean_val = "0x" + value.upper().replace("&H", "")
                        self.address[key.lower()] = int(clean_val, 16)
                    except: self.address[key.lower()] = value
                else:
                    try: self.address[key.lower()] = int(value)
                    except: self.address[key.lower()] = value
            return True
        return False

    def get_addr(self, key):
        return self.address.get(key.lower(), 0)

config_data = Settings()