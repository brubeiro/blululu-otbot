from settings import config_data

def testar_leitura():
    print("=== TESTE DE LEITURA DE CONFIGURAÇÕES ===")
    
    # 1. Testar se o nome do processo foi lido
    processo = config_data.get_addr('txtbaseaddress')
    print(f"Nome do Processo: {processo}")

    # 2. Testar conversão de &H000B680D0 para Inteiro
    local_player = config_data.get_addr('txtadrlocalplayer')
    print(f"Base LocalPlayer: {hex(local_player) if isinstance(local_player, int) else 'ERRO'} ({local_player})")

    # 3. Testar Offsets de HP e Mana
    hp_offset = config_data.get_addr('txttibia_healthoffset')
    mp_offset = config_data.get_addr('txttibia_manaoffset')
    
    print(f"Offset HP: {hex(hp_offset) if isinstance(hp_offset, int) else 'ERRO'}")
    print(f"Offset Mana: {hex(mp_offset) if isinstance(mp_offset, int) else 'ERRO'}")

    # 4. Testar Light Offset
    light = config_data.get_addr('txtlightoffset')
    print(f"Offset Light: {hex(light) if isinstance(light, int) else 'ERRO'}")

    print("\n" + "="*40)
    if isinstance(hp_offset, int) and hp_offset > 0:
        print("✅ SUCESSO: Os valores hexadecimais foram convertidos corretamente!")
    else:
        print("❌ ERRO: Verifica se o teu config.ini está na mesma pasta e se as chaves estão corretas.")

if __name__ == "__main__":
    testar_leitura()