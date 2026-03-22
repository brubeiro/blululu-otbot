import ctypes
from pymem import Pymem
from settings import config_data

class MemoryManager:
    def __init__(self):
        self.pm = None
        self.module_base = 0
        self.base_address = 0
        self.is_64bit = False

    def connect(self):
        try:
            process_name = str(config_data.get_addr('txtbaseaddress'))
            static_offset = config_data.get_addr('txtadrlocalplayer')
            
            self.pm = Pymem(process_name)
            self.module_base = self.pm.base_address
            
            # --- DETECÇÃO PRECISA DE 64-BIT ---
            # IsWow64Process retorna True se um processo 32-bit está rodando em Windows 64-bit.
            # Se retornar False em um Windows 64-bit, o processo alvo é 64-bit nativo.
            is_wow64 = ctypes.c_int()
            ctypes.windll.kernel32.IsWow64Process(self.pm.process_handle, ctypes.byref(is_wow64))
            self.is_64bit = not is_wow64.value
            
            # Cálculo do endereço base do player local
            self.base_address = self.module_base + (static_offset if isinstance(static_offset, int) else 0)
            
            arch = "x64" if self.is_64bit else "x32"
            return True, f"Conectado: {process_name} ({arch})"
        except Exception as e:
            return False, f"Erro ao conectar: {str(e)}"

    def get_player_base(self):
        """Lê o ponteiro base do jogador considerando a arquitetura"""
        try:
            if not self.pm or self.base_address == 0: 
                return 0
            
            if self.is_64bit:
                # Em 64 bits, endereços de memória têm 8 bytes (longlong)
                ptr_value = self.pm.read_longlong(self.base_address)
            else:
                # Em 32 bits, endereços de memória têm 4 bytes (uint)
                ptr_value = self.pm.read_uint(self.base_address)
                
            return ptr_value if ptr_value > 0 else 0
        except: 
            return 0

    def read_pointer_chain(self, base_offset, offsets):
        """Percorre uma lista de offsets (Pointer Path)"""
        try:
            if not base_offset or not offsets: 
                return 0
            
            if self.is_64bit:
                addr = self.pm.read_longlong(self.module_base + base_offset)
                for offset in offsets[:-1]:
                    addr = self.pm.read_longlong(addr + offset)
            else:
                addr = self.pm.read_uint(self.module_base + base_offset)
                for offset in offsets[:-1]:
                    addr = self.pm.read_uint(addr + offset)
            
            # O valor final geralmente é um inteiro de 4 bytes (como coordenada ou ID)
            return self.pm.read_int(addr + offsets[-1])
        except: 
            return 0

    def read_uint(self, addr):
        """Leitura genérica de 4 bytes"""
        try: 
            return self.pm.read_uint(addr) if addr > 0 else 0
        except: 
            return 0

    def read_double(self, addr):
        """Leitura de valores flutuantes de 8 bytes (comum para HP/Mana no OTC)"""
        try:
            if not self.pm or addr <= 0: 
                return 0
            val = self.pm.read_double(addr)
            # Filtro de sanidade: HP/Mana raramente passam de 200k em OTs comuns
            return int(val) if 0 <= val < 200000 else 0
        except: 
            return 0