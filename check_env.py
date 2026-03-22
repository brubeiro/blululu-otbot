import platform
import sys
import struct

def verificar_ambiente():
    print("=== DIAGNÓSTICO DE AMBIENTE BLULULURIFT ===")
    
    # 1. Verifica a arquitetura do Python
    arch_bits = struct.calcsize("P") * 8
    print(f"Arquitetura do Python: {arch_bits}-bit")
    
    # 2. Verifica o Sistema Operacional
    os_info = platform.architecture()[0]
    print(f"Sistema Operacional: {platform.system()} {os_info}")
    
    # 3. Veredito para o Zamonia
    print("\n--- RESULTADO ---")
    if arch_bits == 64:
        print("✅ TUDO OK! Seu Python é 64-bit e pode ler o Zamonia.")
    else:
        print("❌ ATENÇÃO: Seu Python é 32-bit.")
        print("Para o Zamonia (64-bit), você PRECISA baixar e instalar o Python x86-64")
        print("em python.org, caso contrário o bot nunca encontrará a memória.")

    print("\nVersão do Python:", sys.version)

if __name__ == "__main__":
    verificar_ambiente()