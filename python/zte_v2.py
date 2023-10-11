import telnetlib
import time

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"

# Endereços IP e seus respectivos nomes pré-definidos da OLT ZTE
enderecos_ip = { 
    "🖥  OLT ZTE PARAISO ➡": "172.31.188.2",
    "🖥  OLT ZTE PALMEIRANDIA ➡": "172.31.249.2"
}

# Mostrar os endereços IP disponíveis
print("Endereços IP disponíveis: ")
for i, (nome, ip) in enumerate(enderecos_ip.items()):
    print(f"{i + 1}. {nome} ({ip})")

# Solicitar ao usuário que escolha um endereço IP
escolha = int(input("Escolha um número de endereço IP: "))
if escolha < 1 or escolha > len(enderecos_ip):
    print("Escolha inválida. Saindo do script")
    exit()

# Selecionar o endereço IP escolhido
host = list(enderecos_ip.values())[escolha - 1]

# Conectando à OLT ZTE via telnet
tn = telnetlib.Telnet(host, port)

# Fazendo login
time.sleep(0.5)
tn.write(usuario.encode('ascii') + b"\n")
time.sleep(0.5)
tn.write(senha.encode('ascii') + b"\n")
time.sleep(0.5)

# Executando o comando "show pon onu uncfg"
time.sleep(0.5)
tn.write(b"configure terminal\n")
time.sleep(0.5)
tn.write(b"show pon onu uncfg\n")
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print("Saída do comando 'show pon onu uncfg':")
print(output)

# Dados de PON
pon_value = input("Informe o valor do campo PON: ")

# Executar o comando "show gpon onu state"
tn.write("show gpon onu state gpon_olt-1/3/{}\n ".format(pon_value).encode('ascii'))
tn.write(b" \n")
time.sleep(0.5)
tn.write(b" \n")
time.sleep(0.5)
tn.write(b" \n")
time.sleep(0.5)
tn.write(b" \n")
time.sleep(0.5)
output = tn.read_very_eager().decode('ascii')
print("Saída do comando 'show gpon onu state':")
print(output)

# Função para executar comandos e  mostrar saída
def executar_comando(tn, comando):
    tn.write(comando.encode('ascii') + b"\n")
    time.sleep(1)
    output = tn.read_very_eager().decode('ascii')
    print(output)

# Dados de Provisionamento
id_onu = input("Informe o valo do campo ID ONU: ")
type_onu = input("Informe o campo type ZTE-F643 ou ZTE-F660: ")
sn_onu = input("Informe o campo da SERIAL: ")
vlan_value = input("Informe o campo da VLAN: ")
name_onu = input("Informe o nome do CLIENTE: ")

# Executando comandos de Provisionamento
executar_comando(tn, f'!')
executar_comando(tn, f"interface gpon_olt-1/3/{pon_value}")
executar_comando(tn, f"onu {id_onu} type {type_onu} sn {sn_onu}")
executar_comando(tn, "exit")
executar_comando(tn, "!")
executar_comando(tn, f"interface gpon_onu-1/3/{pon_value}:{id_onu}")
executar_comando(tn, f"name {name_onu}")
executar_comando(tn, f"sn-bind enable sn")
executar_comando(tn, f"tcont 4 profile 1G")
executar_comando(tn, f"gemport 1 tcont 4")
executar_comando(tn, "exit")
executar_comando(tn, "!")
executar_comando(tn, f"interface vport-1/3/{pon_value}.{id_onu}:1")
executar_comando(tn, f"service-port 1 user-vlan {vlan_value} vlan {vlan_value}")
executar_comando(tn, "exit")
executar_comando(tn, "!")
executar_comando(tn, f"pon-onu-mng gpon_onu-1/3/{pon_value}:{id_onu}")
executar_comando(tn, f"service 1 gemport 1 vlan {vlan_value}")
executar_comando(tn, f"vlan port eth_0/1 mode tag vlan {vlan_value}")
executar_comando(tn, "exit")
executar_comando(tn, "exit")

# Executar o comando "show pon power attenuation"
tn.write("show pon power attenuation gpon_onu-1/3/{}:{}\n".format(pon_value, id_onu).encode('ascii'))
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print(output)

# Fechando a conexão Telnet
tn.close()

print("Provisionamento concluído 😎 ✅ ✅ ✅ ")
