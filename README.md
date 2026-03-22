# Blululu OTBot 🤖

O **Blululu OTBot** é uma ferramenta de automação e suporte desenvolvida para o **OTClient v8**. O projeto foca no estudo de manipulação de memória e interação com processos em tempo real, oferecendo uma interface intuitiva para otimização de gameplay.

## 🚀 Funcionalidades

* **Memory Reading Engine:** Leitura de endereços de memória (offsets/pointers) para monitoramento de HP, Mana e Status.
* **Suporte Multi-Arquitetura:** Desenvolvido com lógica adaptável para clientes **x32** e **x64**.
* **Auto-Healing:** Sistema inteligente de cura baseado em prioridades e intervalos configuráveis.
* **Interface Customizada:** GUI integrada para fácil configuração das funções de suporte.
* **Integração com Pymem:** Utilização de bibliotecas Python de alto desempenho para manipulação de memória.

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal do projeto.
* **Pymem:** Para leitura e escrita na memória do processo.
* **PyQt / Tkinter:** Para o desenvolvimento da interface gráfica (GUI).
* **Cheat Engine:** Utilizado na fase de mapeamento de ponteiros dinâmicos.

## 📂 Estrutura do Projeto

* `/src`: Código-fonte principal do bot.
* `/offsets`: Arquivos de configuração com os endereços de memória para diferentes versões do OTClient.
* `/modules`: Lógicas específicas de cura, utilitários e automação.

## ⚠️ Aviso Legal (Disclaimer)

Este projeto foi desenvolvido estritamente para **fins educacionais** e de estudo sobre Engenharia de Software, especificamente focado em manipulação de processos e memória. O uso de ferramentas de automação pode violar os termos de serviço de determinados servidores. O desenvolvedor não se responsabiliza pelo uso indevido desta ferramenta.

---
Desenvolvido por [Bruno Ribeiro](https://github.com/brubeiro)