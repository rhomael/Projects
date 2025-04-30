import telnetlib3
import asyncio

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"

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

# Função para executar comandos e mostrar saída
async def executar_comando(writer, comando):
    writer.write(comando + "\n")
    await writer.drain()
    await asyncio.sleep(3)

async def shell(reader, writer):
    # Função shell vazia para evitar erros
    pass

async def main():
    # Conectando à OLT Huawei via Telnet
    reader, writer = await telnetlib3.open_connection(
        host, port=port, shell=shell  # Define a função shell corretamente
    )

    # Fazendo login
    await asyncio.sleep(1)
    writer.write(usuario + "\n")
    await writer.drain()
    await asyncio.sleep(1)
    writer.write(senha + "\n")
    await writer.drain()
    await asyncio.sleep(1)

    # Executando o comando "display ont autofind all"
    await executar_comando(writer, "enable")
    await executar_comando(writer, "config")
    writer.write("display ont autofind all\n")
    await writer.drain()
    await asyncio.sleep(3)

    output = await reader.read(1024)
    print("Saída do comando 'display ont autofind all':")
    print(output)

    # Exibindo o comando e a mensagem de falha
    print("\n  Command:")
    print("          display ont autofind all")
    print("  Failure: The automatically found ONTs do not exist")

    # Dados de provisionamento
    slot_value = input("Informe o valor do campo SLOT: ")
    pon_value = input("Informe o valor do campo PON: ")
    id_value = input("Informe o valor do campo ID SERIAL: ")
    veip_value = input("Informe o valor do campo VEIP 30,300 ou 40,1022: ")
    vlan_value = input("Informe o valor do campo VLAN: ")
    desc_value = input("Informe o valor do campo DESCRIÇÃO: ")

    # Execução dos comandos de provisionamento
    await executar_comando(writer, f"interface gpon 0/{slot_value}")
    await executar_comando(writer, f"ont confirm {pon_value} sn-auth {id_value} omci ont-lineprofile-id {veip_value} ont-srvprofile-id {vlan_value} desc {desc_value}")
    onu_value = input("Informe o valor do campo ID ONU: ")
    await executar_comando(writer, f"ont port native-vlan {pon_value} {onu_value} eth 1 vlan {vlan_value}")
    await executar_comando(writer, "quit")
    await executar_comando(writer, f"service-port vlan {vlan_value} gpon 0/{slot_value}/{pon_value} ont {onu_value} gemport 5 multi-service user-vlan {vlan_value}")

    # Executar o comando "display ont optical-info "
    await executar_comando(writer, f"interface gpon 0/{slot_value}")
    await executar_comando(writer, f"display ont optical-info {pon_value} {onu_value}")

    output = await reader.read(1024)
    print(output)

    # Fechando a conexão Telnet
    writer.close()
    await writer.wait_closed()

    print("Provisionamento concluído 😎 ✅ ✅ ✅ ")

# Executar o script asyncio
asyncio.run(main())