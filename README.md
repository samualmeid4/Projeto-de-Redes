# 🌐 Telemetria & Monitoramento de Máquinas via Sockets SSL/TLS

Aplicação cliente-servidor para coleta remota e monitoramento de métricas de sistema (CPU, RAM, Disco e Hostname) em tempo real, utilizando sockets seguros com **Python**, criptografia **SSL/TLS** e serialização binária com **Pickle/Struct**.

---

## 🎯 Destaques do Projeto
* **Comunicação Segura:** Canal criptografado via certificados SSL/TLS garantindo privacidade e autenticidade.
* **Monitoramento de Hardware:** Leitura de métricas de desempenho em tempo real utilizando a biblioteca `psutil`.
* **Protocolo de Aplicação Próprio:** Enquadramento de mensagens com cabeçalho de tamanho fixo (`struct`) e payload binário (`pickle`).

---

## 🛠️ Tecnologias
* **Linguagem:** Python 3
* **Protocolos:** TCP Sockets com camada de segurança SSL/TLS
* **Bibliotecas:** `socket`, `ssl`, `psutil`, `pickle`, `struct`, `platform`

---

## 📁 Estrutura de Diretórios
```text
Projeto-de-Redes/
└── Projeto de Redes/
    ├── Cliente/
    │   └── cliente.py   # Coleta métricas locais e transmite ao servidor
    ├── Servidor/
    │   └── servidor.py  # Recebe conexões seguras, processa e exibe métricas
    ├── comum/
    │   └── dados.py     # Estrutura compartilhada InfoCliente
    └── solução/         # Scripts auxiliares e certificados
```

---

## 🚀 Como Executar

### 1. Iniciar o Servidor
```bash
cd "Projeto de Redes/Servidor"
python servidor.py
```

### 2. Iniciar o Cliente
Em outro terminal:
```bash
cd "Projeto de Redes/Cliente"
python cliente.py
```

---

## 👨‍💻 Autor
Desenvolvido por [Samuel de Almeida Sousa](https://github.com/samualmeid4).
