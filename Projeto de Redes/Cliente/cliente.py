import socket
import ssl
import platform
import psutil
import pickle
import struct
from dados import InfoCliente

def coletar_info():
    hostname = platform.node()
    cpu = psutil.cpu_count(logical=True)
    ram_livre = int(psutil.virtual_memory().available / (1024 * 1024))
    disco_livre = int(psutil.disk_usage('/').free / (1024 * 1024))
    ips = socket.gethostbyname_ex(socket.gethostname())[2]

    interfaces = psutil.net_if_stats()
    interfaces_inativas = [nome for nome, stat in interfaces.items() if not stat.isup]

    conexoes = psutil.net_connections()
    portas = list({conexao.laddr.port for conexao in conexoes if conexao.status == 'LISTEN'})

    return InfoCliente(hostname, cpu, ram_livre, disco_livre, ips, interfaces_inativas, portas)

def exibir_menu():
    print("\nEscolha o que deseja visualizar:")
    print("1 - Quantidade de processadores")
    print("2 - Memória RAM livre")
    print("3 - Espaço em disco livre")
    print("4 - Endereço IP das interfaces")
    print("5 - Mostrar interfaces desativadas")
    print("6 - Listar portas TCP/UDP abertas")
    print("7 - Mostrar médias dos dados dos clientes")
    print("8 - Listar e detalhar um cliente específico")
    return input("Digite o número da opção: ")

def enviar_pacote(sock, obj):
    msg = pickle.dumps(obj)
    sock.sendall(struct.pack('>I', len(msg)) + msg)

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

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection(('localhost', 8443)) as sock:
    with context.wrap_socket(sock, server_hostname='localhost') as ssock:
        info = coletar_info()
        opcao = exibir_menu()
        pacote = {'info': info, 'opcao': opcao}
        enviar_pacote(ssock, pacote)

        resposta = receber_pacote(ssock)
        print("\n🔍 Resposta do servidor:")
        print(resposta)
