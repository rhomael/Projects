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

# Conectando à OLT ZTE via Telnet
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
sn_onu = input("Informe o valor do campo SERIAL: ")

# Executar o comando "show gpon onu by sn"
tn.write("show gpon onu by sn {}\n ".format(sn_onu).encode('ascii'))
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print(output)

# Função para executar comandos e mostrar saída
def executar_comando(tn, comando):
    tn.write(comando.encode('ascii') + b"\n")
    time.sleep(1)
    output = tn.read_very_eager().decode('ascii')
    print(output)

# Dados de Desprovisionamento
pon_value = input("Informe o valor do campo PON: ")
id_onu = input("Informe o valor do campo ID ONU: ")

# Executando comandos de Desprovisionamento
executar_comando(tn, f"interface gpon_olt-1/3/{pon_value}")
executar_comando(tn, f"no onu {id_onu}")

print("Desprovisionamento concluído 😎 ✅ ✅ ✅ ")
