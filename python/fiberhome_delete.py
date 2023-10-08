import telnetlib
import time

# Dados de login da OLT Fiberhome 🔑
usuario = "GEPON"
port = "23"
senha = "admin1!"
senha_enable = "admin1!"

# Endereços IP e seus respectivos nomes pré-definidos da OLT Fiberhome
enderecos_ip = {
    "🖥  OLT PINHEIRO ➡": "172.31.255.3",
    "🖥  OLT SÃO LUIS ➡": "172.30.247.100",
    "🖥  OLT SAO BENTO ➡": "172.31.254.2",
    "🖥  OLT TURIACU ➡": "172.31.200.254",
    "🖥  OLT SANTA HELENA ➡": "172.30.253.254",
    "🖥  OLT PEDRO DO ROSARIO ➡": "172.31.246.2",
    "🖥  OLT PACAS ➡": "172.31.191.2",
    "🖥  OLT PRESIDENTE SARNEY ➡": "172.31.252.3",
    "🖥  OLT CONECTA ➡": "177.66.195.157"
}

# Mostrar os endereços IP disponíveis
print("Endereços IP disponíveis:")
for i, (nome, ip) in enumerate(enderecos_ip.items()):
    print(f"{i+1}. {nome} ({ip})")

# Solicitar ao usuario que escolha um endereço IP
escolha = int(input("Escolha um número de endereço IP: "))
if escolha < 1 or escolha > len(enderecos_ip):
    print("Escolha inválida. Saindo do script.")
    exit()

# Selecionar o endereço IP escolhido
host = list(enderecos_ip.values())[escolha - 1]

# Comandos de desprovisionamento
comandos_desprovisionamento = [
    "set whitelist phy_addr address {0} password null action delete\n"
]

# Conectando à OLT Fiberhome via Telnet
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

# Executando o comando "cd onu"
tn.write(b"cd onu\n")
time.sleep(1)
output = tn.read_very_eager().decode('ascii')
print(output)

# Atualizando os campos em Dados de provisionamento
id_value = input("Informe o valor do campo ID: ")

# Executar o comando "set whitelist delete"
tn.write("set whitelist phy_addr address {0} password null action delete\n".format(id_value).encode('ascii'))
time.sleep(1)
output = tn.read_very_eager().decode('ascii')
print(output)

# Executando os comandos de desprovisionamento
for comando_desprovisionamento in comandos_desprovisionamento:
    comando_desprovisionamento = comando_desprovisionamento.format(id_value)

    tn.write(comando_desprovisionamento.encode('ascii') + b"\n")
    time.sleep(1.5)
    output = tn.read_very_eager().decode('ascii')
    print(output)

# Fechando a conexão Telnet
tn.close

print("Desprovisionamento concluído 😎 ✅ ✅ ✅ ")
