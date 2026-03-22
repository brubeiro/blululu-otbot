# 🍔 Blululu Rift - Ultimate V3

**Blululu Rift** é um bot modular de alta performance desenvolvido em Python para automação de tarefas em jogos (MMORPGs). O projeto utiliza leitura de memória em tempo real para monitorizar atributos do personagem e reagir instantaneamente.

---

## Funcionalidades

- 🛡️ **Auto-Heal & Auto-Potion:** Cura automática baseada em valores reais de HP e Mana.
- ✨ **Mana Train:** Treino de skills automatizado quando a mana atinge o limite.
- 🍕 **Auto-Food:** Sistema de alimentação cíclico (loop de 5 min).
- 🔄 **Anti-AFK:** Sistema de rotação para evitar desconexão por inatividade.
- 💡 **Light Hack:** Modificação de memória para iluminação total do mapa.
- 🔒 **Security Lock:** Só envia comandos de teclado se a janela do jogo estiver em foco.
- ⚙️ **Sistema Modular:** Configurações técnicas via `config.ini` e perfis de usuário via JSON.

---

## Como Utilizar

1. **Configuração Técnica:** - Edite o ficheiro `config.ini` com os endereços de memória (offsets) atualizados do seu jogo.
2. **Execução:** - Execute o `main.exe` (ou `python main.py`) como **Administrador**.
3. **Perfis:** - Digite o nome do seu personagem na interface, ajuste os valores e clique em **Salvar**.

---

## Tecnologias Utilizadas

- **Python 3.11+**
- **PyQt5:** Interface Gráfica (GUI).
- **Pymem:** Manipulação e leitura de memória RAM.
- **PyDirectInput:** Simulação de teclas em baixo nível (DirectX compatível).
- **PyGetWindow:** Gestão e verificação de janelas ativas.

---

## Créditos e Autoria

Este projeto foi desenvolvido e idealizado por:

* **Bruno Ribeiro** **Brubeiro** - *Desenvolvimento Principal e Arquitetura* - [https://github.com/brubeiro]

---

## Aviso Legal

Este software foi criado para fins de estudo e automação pessoal. O uso de bots pode violar os Termos de Serviço de alguns jogos. Use com responsabilidade. O autor não se responsabiliza por eventuais suspensões ou banimentos.