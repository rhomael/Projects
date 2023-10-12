import telnetlib
import time

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"

# Endereços IP e seus respectivos nomes pré-definidos da OLT Intelbras
enderecos_ip = {
    "🖥  OLT INTELBRAS BOM_VIVER ➡": "172.31.248.2",
    "🖥  OLT INTELBRAS FORTALEZA ➡": "172.31.194.2"
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

# Conectando à OLT Intelbras via Telnet
tn = telnetlib.Telnet(host, port)

# Fazendo login
tn.write(usuario.encode('ascii') + b"\n")
tn.write(senha.encode('ascii') + b"\n")

# Executando o comando "show ont-find list interface gpon all"
tn.write(b"enable\n")
tn.write(b"configure terminal\n")
tn.write(b"show ont-find list interface gpon all\n")
time.sleep(3)

output = tn.read_very_eager().decode('ascii')
print("Saída do comando 'show ont-find list interface gpon all':")
print(output)

# Função para executar comandos e mostrar saída
def executar_comando(tn, comando):
    tn.write(comando.encode('ascii') + b"\n")
    time.sleep(3)
    output = tn.read_very_eager().decode('ascii')
    print(output)

# Dados de provisionamento
sn_value = input("Informe o valor do campo ID Serial: ")

# Executando o comando "show ont brief sn string-hex"
time.sleep(1)
tn.write("show ont brief sn string-hex {}\n".format(sn_value).encode('ascii'))
tn.write(b"\n")
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print("show ont brief sn string-hex':")
print(output)

# Dados dos comandos de provisionamento
pon_value = input("Informe o valor do campo PON: ")
id_value = input("Informe o valor do campo ID: ")
desc_value = input("Informe o valor do campo Nome: ")
veip_value = input("Informe o valor do campo VEIP: ")

# Execução dos comandos de provisionamento
executar_comando(tn, f"interface gpon 0/{pon_value}")
executar_comando(tn, "deploy profile rule")
executar_comando(tn, f"aim 0/{pon_value}/{id_value} name {desc_value}")
executar_comando(tn, f"permit sn string-hex {sn_value} line {veip_value} default line {veip_value}")
executar_comando(tn, f"active")
executar_comando(tn, "y")
executar_comando(tn, "exit")
executar_comando(tn, "end")

# Executar o comando "show ont optical-info"
time.sleep(1)
tn.write("show ont optical-info 0/{}/{}\n".format(pon_value, id_value).encode('ascii'))
time.sleep(3)
output = tn.read_very_eager().decode('ascii')
print(output)

# Fechando a conexão Telnet
tn.close()

print("Provisionamento concluído 😎 ✅ ✅ ✅ ")
