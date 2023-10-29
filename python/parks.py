import telnetlib
import time

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23" #port = "4023"  # PORTA TELNET OLT CONECTA

# Endereços IP e seus respectivos nomes pré-definidos da OLT Parks
enderecos_ip = {
    "🖥  OLT PARKS CONECTA ➡": "177.66.195.157"
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

# Conectando à OLT Fiberhome via Telnet
tn = telnetlib.Telnet(host, port)

# Fazendo login
tn.write(b"\n")
tn.read_until(b"Username: ")
tn.write(usuario.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(senha.encode('ascii') + b"\n")

# Executando o comando "sh gpon onu unconfigured"
tn.write(b"\n")
tn.write(b"sh gpon onu unconfigured\n")
time.sleep(5)  # Aguardar tempo suficiente para o retorno ser obtido
output = tn.read_very_eager().decode('ascii')
print("Saída do comando 'show gpon onu unconfigured'")
print(output)
tn.write(b"\n")

# Função para executar comandos e mostrar saída
def executar_comando(tn, comando):
    tn.write(comando.encode('ascii') + b"\n")
    time.sleep(3)
    output = tn.read_very_eager().decode('ascii')
    print(output)

# Dados de provisionamento
slot_value = input("Informe o valor do campo SLOT: ")
pon_value = input("Informe o valor do campo PON: ")
alias_value = input("Informe o valor do campo NOME DO CLIENTE: ")
serial_value = input("Informe o valor do SERIAL ONU: ")
uniport_value = input("Informe o valor do UNIPORT 1 ou 1-4: ")
veip_value = input("Informe o valor BRIDGE ou ROUTER: ")
vlan_value = input("Informe o valor da VLAN: ")

# Execução dos comandos de provisionamento
time.sleep(1)
executar_comando(tn, "configure terminal")
time.sleep(1)
executar_comando(tn, f"interface gpon{slot_value}/{pon_value}")
time.sleep(1)
executar_comando(tn, f"onu {serial_value} alias {alias_value}")
time.sleep(1)
executar_comando(tn, f"onu {serial_value} ethernet-profile auto-on uni-port {uniport_value}")
time.sleep(1)
executar_comando(tn, f"onu {serial_value} flow-profile onu_{veip_value}_vlan_{vlan_value}_pon{pon_value}")
time.sleep(1)
executar_comando(tn, f"onu {serial_value} vlan-translation-profile _{vlan_value} uni-port 1")
time.sleep(1)
executar_comando(tn, "end")

# Executar o comando "show gpon onu 'serial' summary"
time.sleep(1)
tn.write("show gpon onu {} summary\n".format(serial_value).encode('ascii'))
time.sleep(5)
output = tn.read_very_eager().decode('ascii')
print(output)

print("Provisionamento concluído 😎 ✅ ✅ ✅")
