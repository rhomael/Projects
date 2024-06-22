import telnetlib
import time
import re

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"
senha_enable = input("Insira a senha enable da OLT: ")

# Endereços IP e seus respectivos nomes pré-definidos da OLT Fiberhome
enderecos_ip = {
    "🖥  OLT PINHEIRO ➡": "172.31.255.3",
    "🖥  OLT SÃO LUIS ➡": "172.30.247.100",
    "🖥  OLT SAO BENTO ➡": "172.31.254.2",
    "🖥  OLT TURIACU ➡": "172.31.200.254",
    "🖥  OLT VILA DA PAZ ➡": "172.31.187.2",
    "🖥  OLT SANTA HELENA ➡": "172.30.253.254",
    "🖥  OLT PEDRO DO ROSARIO ➡": "172.31.246.2",
    "🖥  OLT PACAS ➡": "172.31.191.2",
    "🖥  OLT PRESIDENTE SARNEY ➡": "172.31.252.3",
    "🖥  OLT CONECTA ➡": "177.66.195.157",
    "🖥  OLT SLP ➡": "172.31.254.2",
    "🖥  OLT MHZ ➡": "172.16.0.2",
    "🖥  OLT GNF ➡": "172.31.253.2"
}

# Mostrar os endereços IP disponíveis
print("Endereços IP disponíveis:")
for i, (nome, ip) in enumerate(enderecos_ip.items()):
    print(f"{i+1}. {nome} ({ip})")

# Solicitar ao usuário que escolha um endereço IP
escolha = int(input("Escolha um número de endereço IP: "))
if escolha < 1 or escolha > len(enderecos_ip):
    print("Escolha inválida. Saindo do script.")
    exit()

# Selecionar o endereço IP escolhido
host = list(enderecos_ip.values())[escolha - 1]

# Conectando a OLT Fiberhome via Telnet
tn = telnetlib.Telnet(host, port)

# Fazendo login
tn.read_until(b"Login: ")
tn.write(usuario.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(senha.encode('ascii') + b"\n")

# Habilitando o modo privilegiado
tn.write(b"enable\n")
tn.read_until(b"Password: ")
tn.write(senha_enable.encode('ascii') + b"\n")

# Executando o comando "cd device"
tn.write(b"cd device\n")
time.sleep(1)
output = tn.read_very_eager().decode('ascii')
print(output)

# Atualizando os campos em Dados de MAC
id_mac = input("Informe o valor do campo MAC: ")

# Executar o comando "show mac_find onu mac_address"
time.sleep(5)
tn.write("show mac_find onu mac_address {0}\n".format(id_mac).encode('ascii'))
time.sleep(40)
output = tn.read_very_eager().decode('ascii')
print(output)

# Fechando a conexão Telnet
tn.close

print("Scan de mac-address concluído 😎 ✅ ✅ ✅ ")
