import socket

def verificar_porta(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # Define um timeout de 2 segundos para a conexão
    resultado = sock.connect_ex((ip, porta))
    sock.close()

    if resultado == 0:
        print(f"A 🚪 {porta} está aberta ✅ no IP {ip} ")
    else:
        print(f"A 🚪 {porta} está fechada ❌ no IP {ip} ")

# Solicitar o IP e a Porta ao usuário
ip = input("Digite o IP que deseja verificar: ")
porta = int(input("Digite a 🚪 que deseja verificar: "))

verificar_porta(ip, porta)
