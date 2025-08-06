# comum/dados.py

class InfoCliente:
    def __init__(self, hostname, cpu, ram_livre, disco_livre, ips, interfaces_inativas, portas):
        self.hostname = hostname
        self.cpu = cpu
        self.ram_livre = ram_livre
        self.disco_livre = disco_livre
        self.ips = ips
        self.interfaces_inativas = interfaces_inativas
        self.portas = portas
