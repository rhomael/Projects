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

# Dados de desprovisionamento
gpon_value = input("Informe o valor da GPON:")
serial_value = input("Informe o valor da SERIAL ONU: ")

# Execução dos comandos de desprovisionamento
executar_comando(tn, "configure terminal")
time.sleep(1)
executar_comando(tn, f"interface gpon{gpon_value}")
time.sleep(1)
executar_comando(tn, f"no onu {serial_value}")
time.sleep(1)
executar_comando(tn, "end")

print("Desprovisionamento concluído 😎 ✅ ✅ ✅")
