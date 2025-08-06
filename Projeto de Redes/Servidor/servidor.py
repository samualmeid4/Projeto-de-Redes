import socket
import ssl
import pickle
import struct
#from comum.dados 
from dados import InfoCliente

clientes = []

def media(lst):
    return round(sum(lst) / len(lst), 2) if lst else 0

def processar_opcao(opcao, hostname=None):
    if opcao == '1':
        return f"Processadores: {[cli.cpu for cli in clientes]}"
    elif opcao == '2':
        return f"RAM Livre (MB): {[cli.ram_livre for cli in clientes]}"
    elif opcao == '3':
        return f"Disco Livre (MB): {[cli.disco_livre for cli in clientes]}"
    elif opcao == '4':
        return f"IPs: {[cli.ips for cli in clientes]}"
    elif opcao == '5':
        return f"Interfaces Inativas: {[cli.interfaces_inativas for cli in clientes]}"
    elif opcao == '6':
        return f"Portas Abertas: {[cli.portas for cli in clientes]}"
    elif opcao == '7':
        return (
            f"Média CPU: {media([c.cpu for c in clientes])}, "
            f"RAM: {media([c.ram_livre for c in clientes])} MB, "
            f"Disco: {media([c.disco_livre for c in clientes])} MB"
        )
    elif opcao == '8':
        if hostname:
            for c in clientes:
                if c.hostname == hostname:
                    return vars(c)
            return f"Cliente '{hostname}' não encontrado."
        else:
            return f"Clientes disponíveis: {[c.hostname for c in clientes]}"
    else:
        return "Opção inválida."

def receber_pacote(sock):
    raw_tamanho = sock.recv(4)
    if not raw_tamanho:
        return None
    tamanho = struct.unpack('>I', raw_tamanho)[0]
    dados = b''
    while len(dados) < tamanho:
        parte = sock.recv(tamanho - len(dados))
        if not parte:
            break
        dados += parte
    return pickle.loads(dados)

def enviar_pacote(sock, obj):
    msg = pickle.dumps(obj)
    sock.sendall(struct.pack('>I', len(msg)) + msg)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.bind(('0.0.0.0', 8443))
    server_sock.listen(5)
    print("🔒 Servidor escutando na porta 8443...")

    while True:
        conn, addr = server_sock.accept()
        with context.wrap_socket(conn, server_side=True) as sslsock:
            print(f"\n📡 Novo cliente: {addr}")
            try:
                pacote = receber_pacote(sslsock)
                info = pacote['info']
                opcao = pacote['opcao']
                hostname = getattr(info, 'hostname', 'desconhecido')

                # Armazena ou atualiza
                clientes = [c for c in clientes if c.hostname != hostname]
                clientes.append(info)

                if opcao == '8':
                    resposta = processar_opcao(opcao)
                else:
                    resposta = processar_opcao(opcao, hostname)

                enviar_pacote(sslsock, resposta)
            except Exception as e:
                print(f"❌ Erro: {e}")
