import telnetlib
import time

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"
#port = "23"  # PORTA TELNET OLT MIRINZAL
#port = "23"  # PORTA TELNET OLT PINHEIRO
#port = "4020"  # PORTA TELNET OLT FIALHO
#port = "4030"  # PORTA TELNET OLT COHAB
#port = "4940"  # PORTA TELNET OLT ITAPECURU
#port = "4950"  # PORTA TELNET OLT SANTA HELENA
#port = "5050"  # PORTAL TELNET OLT TURIACU

# Endereços IP e seus respectivos nomes pré-definidos da OLT Huawei
enderecos_ip = {
    "🖥  OLT HUWAEI COHAB ➡": "186.216.11.0",
    "🖥  OLT HUWAEI ITAPECURU ➡": "45.181.228.67",
    "🖥  OLT HUWAEI FIALHO ➡": "186.216.11.0",
    "🖥  OLT HUWAEI PINHEIRO ➡": "172.31.237.2",
    "🖥  OLT HUAWEI MIRINZAL ➡": "172.31.238.2",
    "🖥  OLT HUWAEI SANTA HELENA ➡": "45.181.230.29",
    "🖥  OLT HUWAEI TURIACU ➡": "186.216.45.254"
}

# Mostra os endereços IP disponíveis
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

# Conectando à OLT Huawei via Telnet
tn = telnetlib.Telnet(host, port)

# Fazendo login
time.sleep(1)
tn.write(usuario.encode('ascii') + b"\n")
time.sleep(1)
tn.write(senha.encode('ascii') + b"\n")
time.sleep(1)

# Executando o comando "display ont autofind all"
time.sleep(1)
tn.write(b"enable\n")
time.sleep(1)
tn.write(b"config\n")
time.sleep(1)
tn.write(b"display ont autofind all\n")
tn.write(b" \n")
time.sleep(3)
tn.write(b" \n")
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print("Saída do comando 'display ont autofind all':")
print(output)

id_value = input("Informe o valor do campo ID SERIAL: ")

# Executando o comando "display ont info by-sn"
time.sleep(1)
tn.write("display ont info by-sn {}\n".format(id_value).encode('ascii'))
tn.write(b"\n")
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print("Saída do comando 'display ont info by-sn':")
print(output)

slot_value = input("Informe o valor do campo SLOT: ")
pon_value = input("Informe o valor do campo PON: ")

# Executando o comando "display service-port port"
time.sleep(1)
tn.write("interface gpon 0/{}\n".format(slot_value).encode('ascii'))
time.sleep(1)
tn.write("display service-port port 0/{}/{}\n".format(slot_value, pon_value).encode('ascii'))
tn.write(b" \n")
time.sleep(3)
tn.write(b" \n")
time.sleep(3)
tn.write(b" \n")
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print("Saída do comando 'display service-port':")
print(output)

id_undo_value = input("Informe o valor do campo ID UNDO: ")

# Executando o comando "undo service-port"
time.sleep(1)
tn.write("undo service-port {}\n".format(id_undo_value).encode('ascii'))
tn.write(b"\n")

onu_value = input("Informe o valor do campo ID ONU: ")

# Função para executar comandos e mostrar saída
def executar_comando(tn, comando):
    tn.write(comando.encode('ascii') + b"\n")
    time.sleep(3)
    output = tn.read_very_eager().decode('ascii')
    print(output)

executar_comando(tn, f"interface gpon 0/{slot_value}")
executar_comando(tn, f"ont delete {pon_value} {onu_value}\n")

# Fechando a conexão Telnet
tn.close()

print("Desprovisionamento concluído 😎 ✅ ✅ ✅ ")
