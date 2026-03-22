import sys, time, ctypes
from PyQt5 import QtWidgets, QtCore, QtGui
from memory import MemoryManager
from worker import BotWorker
from settings import config_data

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class BlululuUltimate(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # ID para agrupar na barra de tarefas
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('blululu.bot.bacon.v1')
        
        self.setWindowTitle("Blululu OTBot")
        self.setFixedSize(850, 950) # Ajustado para caber tudo confortavelmente
        self.setWindowIcon(QtGui.QIcon('bacon.ico')) 
        
        self.mem = MemoryManager()
        self.worker = BotWorker(self.mem)
        
        # Tabela de Cores do Light Hack (Bytes para o OTClient)
        self.light_colors = {
            "Branco": 215, 
            "Amarelo": 208, 
            "Vermelho": 192, 
            "Verde": 66, 
            "Azul": 5,
            "Laranja": 198,
            "Roxo": 150
        }
        
        self.init_ui()
        
        # Sinais
        self.worker.stats_signal.connect(self.update_ui_stats)
        self.worker.log_signal.connect(lambda m: self.log.append(f"[{time.strftime('%H:%M:%S')}] {m}"))
        self.worker.start()

    def init_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)
        
        # --- COLUNA 1: CONFIGURAÇÕES ---
        col1 = QtWidgets.QVBoxLayout()
        
        # Grupo Server
        serv_gb = QtWidgets.QGroupBox("🌐 Server")
        self.cmb_server = QtWidgets.QComboBox()
        self.cmb_server.addItems(config_data.all_servers)
        self.btn_conn = QtWidgets.QPushButton("🚀 CONECTAR AO JOGO")
        self.btn_conn.setFixedHeight(45)
        self.btn_conn.setStyleSheet("font-weight: bold; background-color: #2ecc71; color: white; font-size: 14px;")
        self.btn_conn.clicked.connect(self.connect_game)
        serv_l = QtWidgets.QVBoxLayout()
        serv_l.addWidget(self.cmb_server)
        serv_l.addWidget(self.btn_conn)
        serv_gb.setLayout(serv_l)
        col1.addWidget(serv_gb)

        # Labels de Status
        st_l = QtWidgets.QHBoxLayout()
        self.lbl_hp = QtWidgets.QLabel("HP: 0")
        self.lbl_mp = QtWidgets.QLabel("MP: 0")
        self.lbl_hp.setStyleSheet("font-size: 22px; color: #c0392b; font-weight: bold;")
        self.lbl_mp.setStyleSheet("font-size: 22px; color: #2980b9; font-weight: bold;")
        st_l.addWidget(self.lbl_hp)
        st_l.addWidget(self.lbl_mp)
        col1.addLayout(st_l)

        # Grupos de Auto-Ações (Heal, Potion, Mana)
        # 1. Auto-Healer
        h_gb = QtWidgets.QGroupBox("🛡️ Auto-Healer")
        h_l = QtWidgets.QFormLayout()
        self.chk_h = QtWidgets.QCheckBox("Ativar Healer")
        self.spn_h = QtWidgets.QSpinBox(); self.spn_h.setMaximum(999999)
        self.cmb_h = QtWidgets.QComboBox(); self.cmb_h.addItems([f"F{i}" for i in range(1, 13)])
        h_l.addRow(self.chk_h)
        h_l.addRow("Heal abaixo de:", self.spn_h)
        h_l.addRow("Tecla:", self.cmb_h)
        h_gb.setLayout(h_l); col1.addWidget(h_gb)

        # 2. Auto-Potion
        p_gb = QtWidgets.QGroupBox("🧪 Auto-Potion")
        p_l = QtWidgets.QFormLayout()
        self.chk_p = QtWidgets.QCheckBox("Ativar Potion")
        self.spn_p = QtWidgets.QSpinBox(); self.spn_p.setMaximum(999999)
        self.cmb_p = QtWidgets.QComboBox(); self.cmb_p.addItems([f"F{i}" for i in range(1, 13)])
        p_l.addRow(self.chk_p)
        p_l.addRow("Mana abaixo de:", self.spn_p)
        p_l.addRow("Tecla:", self.cmb_p)
        p_gb.setLayout(p_l); col1.addWidget(p_gb)

        # 3. Mana Train
        m_gb = QtWidgets.QGroupBox("✨ Mana Train")
        m_l = QtWidgets.QFormLayout()
        self.chk_m = QtWidgets.QCheckBox("Ativar Mana Train")
        self.spn_m = QtWidgets.QSpinBox(); self.spn_m.setMaximum(999999)
        self.cmb_m = QtWidgets.QComboBox(); self.cmb_m.addItems([f"F{i}" for i in range(1, 13)])
        m_l.addRow(self.chk_m)
        m_l.addRow("Mana acima de:", self.spn_m)
        m_l.addRow("Tecla:", self.cmb_m)
        m_gb.setLayout(m_l); col1.addWidget(m_gb)

        # --- UTILIDADES ---
        util_gb = QtWidgets.QGroupBox("🛠️ Utilidades")
        self.chk_f = QtWidgets.QCheckBox("Auto Eat Food")
        self.cmb_f = QtWidgets.QComboBox(); self.cmb_f.addItems([f"F{i}" for i in range(1, 13)])
        self.chk_a = QtWidgets.QCheckBox("Anti-Idle (Dance)")
        
        # Light Hack Completo
        self.chk_light = QtWidgets.QCheckBox("Light Hack (Full)")
        self.cmb_light_color = QtWidgets.QComboBox()
        self.cmb_light_color.addItems(self.light_colors.keys())
        
        util_l = QtWidgets.QGridLayout()
        util_l.addWidget(self.chk_f, 0, 0); util_l.addWidget(self.cmb_f, 0, 1)
        util_l.addWidget(self.chk_a, 1, 0)
        util_l.addWidget(self.chk_light, 2, 0); util_l.addWidget(self.cmb_light_color, 2, 1)
        util_gb.setLayout(util_l)
        col1.addWidget(util_gb)
        
        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(120)
        self.log.setStyleSheet("background-color: #2c3e50; color: #ecf0f1; font-family: Consolas;")
        col1.addWidget(self.log)
        layout.addLayout(col1)

        # --- COLUNA 2: CAVEBOT E TARGET ---
        col2 = QtWidgets.QVBoxLayout()
        
        # Targeting
        target_gb = QtWidgets.QGroupBox("🎯 Targeting & Loot")
        self.chk_target = QtWidgets.QCheckBox("Ativar Targeting")
        self.txt_target_name = QtWidgets.QLineEdit()
        self.txt_target_name.setPlaceholderText("Ex: Rat, Dragon, Demon...")
        self.chk_loot = QtWidgets.QCheckBox("Auto-Loot (Grid 3x3)")
        target_l = QtWidgets.QVBoxLayout()
        target_l.addWidget(self.chk_target)
        target_l.addWidget(QtWidgets.QLabel("Nome do Monstro:"))
        target_l.addWidget(self.txt_target_name)
        target_l.addWidget(self.chk_loot)
        target_gb.setLayout(target_l)
        col2.addWidget(target_gb)

        # Cavebot
        cave_gb = QtWidgets.QGroupBox("🤖 Cavebot Waypoints")
        cave_l = QtWidgets.QVBoxLayout()
        self.chk_cave = QtWidgets.QCheckBox("Ativar Cavebot")
        self.lst_wps = QtWidgets.QListWidget()
        cave_l.addWidget(self.chk_cave)
        cave_l.addWidget(self.lst_wps)

        btn_grid = QtWidgets.QGridLayout()
        ops = ["Stand", "Node", "Rope", "Shovel", "Pick", "Door", "Ladder"]
        for i, name in enumerate(ops):
            btn = QtWidgets.QPushButton(name)
            btn.clicked.connect(lambda checked, n=name: self.add_wp_type(n))
            btn_grid.addWidget(btn, i//2, i%2)
        
        btn_clear = QtWidgets.QPushButton("Limpar Tudo")
        btn_clear.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        btn_clear.clicked.connect(self.lst_wps.clear)
        btn_grid.addWidget(btn_clear, 4, 0, 1, 2)
        
        cave_l.addLayout(btn_grid)
        cave_gb.setLayout(cave_l)
        col2.addWidget(cave_gb)
        
        layout.addLayout(col2)

    def add_wp_type(self, type_name):
        x, y, z = self.worker.get_coords()
        if x != 0:
            self.lst_wps.addItem(f"{type_name}|{x}|{y}|{z}")
        else:
            self.log.append("Erro: Impossível ler coordenadas agora.")

    def connect_game(self):
        config_data.set_server(self.cmb_server.currentText())
        res, msg = self.mem.connect()
        self.log.append(msg)
        if res:
            self.btn_conn.setText("✅ CONECTADO")
            self.btn_conn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")

    def update_ui_stats(self, data):
        self.lbl_hp.setText(f"HP: {data['hp']}")
        self.lbl_mp.setText(f"MP: {data['mp']}")
        
        # Sincronização em tempo real das configurações para o Worker
        self.worker.config.update({
            "h_act": self.chk_h.isChecked(), "h_at": self.spn_h.value(), "h_key": self.cmb_h.currentText(),
            "p_act": self.chk_p.isChecked(), "p_at": self.spn_p.value(), "p_key": self.cmb_p.currentText(),
            "m_act": self.chk_m.isChecked(), "m_at": self.spn_m.value(), "m_key": self.cmb_m.currentText(),
            "f_act": self.chk_f.isChecked(), "f_key": self.cmb_f.currentText(),
            "a_act": self.chk_a.isChecked(), 
            "light_act": self.chk_light.isChecked(),
            "light_color_val": self.light_colors[self.cmb_light_color.currentText()],
            "target_act": self.chk_target.isChecked(), "target_name": self.txt_target_name.text(), 
            "loot_act": self.chk_loot.isChecked(), 
            "cave_act": self.chk_cave.isChecked(),
            "waypoints": [self.lst_wps.item(i).text() for i in range(self.lst_wps.count())]
        })

if __name__ == "__main__":
    if not is_admin():
        # Re-lança o script como Administrador
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    app = QtWidgets.QApplication(sys.argv)
    # Estilo Dark opcional para melhor visualização
    app.setStyle("Fusion")
    win = BlululuUltimate()
    win.show()
    sys.exit(app.exec_())