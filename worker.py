import time, pydirectinput
import pygetwindow as gw
from PyQt5 import QtCore
from settings import config_data

class BotWorker(QtCore.QThread):
    stats_signal = QtCore.pyqtSignal(dict)
    log_signal = QtCore.pyqtSignal(str)

    def __init__(self, mem):
        super().__init__()
        self.mem = mem
        self.running = True
        self.config = {}
        self.last_food = 0
        self.last_afk = 0
        self.current_wp_idx = 0
        self.loot_offsets = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]

    def is_game_focused(self):
        try:
            target_title = str(config_data.get_addr('txtpartialcap'))
            active_window = gw.getActiveWindow()
            return active_window and target_title.lower() in active_window.title.lower()
        except: return False

    def get_coords(self):
        """Suporta Zamonia (offsets diretos) e ShadowIllusion (pointer chains)"""
        try:
            p_base = self.mem.get_player_base()
            
            # 1. Tenta método Zamonia/Global (Offsets diretos do Player Base)
            off_x = config_data.get_addr('txtmyposxoffset')
            off_y = config_data.get_addr('txtmyposyoffset')
            off_z = config_data.get_addr('txtmyposzoffset')

            if p_base > 0 and off_x > 0:
                x = self.mem.pm.read_int(p_base + off_x)
                y = self.mem.pm.read_int(p_base + off_y)
                z = self.mem.pm.read_int(p_base + off_z)
                return x, y, z

            # 2. Tentar método Pointer Chain (ShadowIllusion)
            b_x = config_data.get_addr('txtposx_base')
            b_y = config_data.get_addr('txtposy_base')
            b_z = config_data.get_addr('txtposz_base')
            p_x = config_data.get_addr('path_x')
            p_y = config_data.get_addr('path_y')
            p_z = config_data.get_addr('path_z')

            if b_x > 0 and p_x:
                parse = lambda p: [int(i.strip(), 16) for i in str(p).split(',')]
                x = self.mem.read_pointer_chain(b_x, parse(p_x))
                y = self.mem.read_pointer_chain(b_y, parse(p_y))
                z = self.mem.read_pointer_chain(b_z, parse(p_z))
                return x, y, z

            return 0, 0, 0
        except: return 0, 0, 0

    def do_loot(self):
        pydirectinput.keyDown('shift')
        w, h = pydirectinput.size()
        cx, cy = w // 2, h // 2
        for dx, dy in self.loot_offsets:
            pydirectinput.rightClick(cx + (dx*38), cy + (dy*38))
            time.sleep(0.01)
        pydirectinput.keyUp('shift')

    def run(self):
        while self.running:
            if self.mem.pm:
                p_base = self.mem.get_player_base()
                if p_base > 0:
                    # --- LEITURA DE STATUS (HP/MP) ---
                    hp = self.mem.read_double(p_base + config_data.get_addr('txttibia_healthoffset'))
                    if hp <= 0:
                        hp = self.mem.pm.read_int(p_base + config_data.get_addr('txttibia_healthoffset'))
                    
                    mp = self.mem.read_double(p_base + config_data.get_addr('txttibia_manaoffset'))
                    if mp <= 0:
                        mp = self.mem.pm.read_int(p_base + config_data.get_addr('txttibia_manaoffset'))
                    
                    # Target Square (Red Square)
                    off_red = config_data.get_addr('txtredsquare')
                    has_target = self.mem.read_uint(self.mem.module_base + off_red) if off_red > 0 else 0
                    
                    self.stats_signal.emit({"hp": hp, "mp": mp})

                    # --- LIGHT HACK DINÂMICO ---
                    off_l = config_data.get_addr('txtlightoffset')
                    off_c = config_data.get_addr('txtcoloroffset')
                    if self.config.get("light_act") and off_l:
                        try:
                            # Brilho (Intensidade)
                            if self.mem.pm.read_uchar(p_base + off_l) < 250:
                                self.mem.pm.write_uchar(p_base + off_l, 250)
                            
                            # Cor (Selecionada via Interface)
                            if off_c > 0:
                                chosen_color = self.config.get("light_color_val", 215)
                                if self.mem.pm.read_uchar(p_base + off_c) != chosen_color:
                                    self.mem.pm.write_uchar(p_base + off_c, chosen_color)
                        except: pass

                    # Verificação de Foco (Pause se não estiver no jogo)
                    if not self.is_game_focused():
                        time.sleep(0.5); continue

                    # --- HEALER ---
                    if hp > 0 and self.config.get("h_act") and hp <= self.config.get("h_at", 0):
                        pydirectinput.press(self.config["h_key"].lower())
                        time.sleep(0.5); continue

                    # --- TARGET & LOOT ---
                    if self.config.get("target_act"):
                        if has_target:
                            time.sleep(0.4); continue
                        else:
                            if self.config.get("loot_act"): self.do_loot()
                            name = self.config.get("target_name")
                            if name:
                                pydirectinput.press('enter')
                                pydirectinput.write(name.lower())
                                pydirectinput.press('enter')
                                time.sleep(0.7)

                    # --- CAVEBOT ---
                    if self.config.get("cave_act") and self.config.get("waypoints") and not has_target:
                        px, py, _ = self.get_coords()
                        if px != 0:
                            wps = self.config["waypoints"]
                            if self.current_wp_idx < len(wps):
                                p = wps[self.current_wp_idx].split('|')
                                tx, ty = int(p[1]), int(p[2])
                                if abs(px-tx) <= 1 and abs(py-ty) <= 1:
                                    self.current_wp_idx += 1
                                else:
                                    if px < tx: pydirectinput.press('right')
                                    elif px > tx: pydirectinput.press('left')
                                    if py < ty: pydirectinput.press('down')
                                    elif py > ty: pydirectinput.press('up')
                            else: self.current_wp_idx = 0

                    # --- AUTO POTION / MANA TRAIN ---
                    if self.config.get("p_act") and mp <= self.config.get("p_at", 0):
                        pydirectinput.press(self.config["p_key"].lower())

                    # --- AUTO FOOD ---
                    if self.config.get("f_act") and (time.time() - self.last_food > 60):
                        pydirectinput.press(self.config["f_key"].lower())
                        self.last_food = time.time()

                    # --- ANTI-IDLE (DANCE) ---
                    if self.config.get("a_act") and (time.time() - self.last_afk > 120):
                        pydirectinput.keyDown('ctrl')
                        pydirectinput.press('down')
                        pydirectinput.press('up')
                        pydirectinput.keyUp('ctrl')
                        self.last_afk = time.time()

            time.sleep(0.1)