import os
import shutil
import subprocess

# Configurações
EXE_NAME = "BlululuRift Bacon version"
MAIN_FILE = "main.py"
ICON_FILE = "bacon.ico"
EXTRA_FILES = ["config.ini", "bacon.ico"] # Arquivos que devem estar ao lado do exe

def build():
    print(f"🚀 Iniciando compilação de {EXE_NAME}...")

    # 1. Executa o PyInstaller
    cmd = [
        'pyinstaller',
        '--noconsole',
        '--onefile',
        f'--icon={ICON_FILE}',
        f'--name={EXE_NAME}',
        MAIN_FILE
    ]
    
    subprocess.run(cmd)

    # 2. Copia os arquivos necessários para a pasta dist
    print("📂 Organizando arquivos extras...")
    for file in EXTRA_FILES:
        if os.path.exists(file):
            shutil.copy(file, os.path.join("dist", file))
            print(f"  - {file} copiado para dist/")

    print(f"\n✅ Concluído! Seu bot está pronto em: {os.path.abspath('dist')}")

if __name__ == "__main__":
    build()