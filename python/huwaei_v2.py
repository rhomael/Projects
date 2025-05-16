import telnetlib3
import asyncio

endereços_ip = {
    "🖥  OLT HUWAEI COHAB ➡": "186.216.11.0",
    "🖥  OLT HUWAEI ITAPECURU ➡": "45.181.228.67",
    "🖥  OLT HUWAEI FIALHO ➡": "186.216.11.0",
    "🖥  OLT HUWAEI PINHEIRO ➡": "172.31.237.2",
    "🖥  OLT HUAWEI MIRINZAL ➡": "172.31.238.2",
    "🖥  OLT HUWAEI SANTA HELENA ➡": "45.181.230.29",
    "🖥  OLT HUWAEI TURIACU ➡": "186.216.45.254"
}

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"

# Mostra os endereços IP disponíveis
print("Endereços IP disponíveis:")
for i, (nome, ip) in enumerate(endereços_ip.items()):
    print(f"{i+1}. {nome} ({ip})")

# Solicitar ao usuário que escolha um endereço IP
escolha = int(input("Escolha um número de endereço IP: "))
if escolha < 1 or escolha > len(endereços_ip):
    print("Escolha inválida. Saindo do script.")
    exit()

# Selecionar o endereço IP escolhido
host = list(endereços_ip.values())[escolha - 1]

# Função para executar comandos e mostrar saída
async def executar_comando(writer, reader, comando, delay=3):
    writer.write(comando + "\n")
    await writer.drain()
    await asyncio.sleep(delay)
    output = await reader.read(2048)
    print(output)

async def listar_interfaces(writer, reader):
    # Executar o comando "display ont interface all"
    await executar_comando(writer, reader, "display ont autofind all", delay=3)
    writer.write(" \n")

async def shell(reader, writer):
    # Função shell vazia para evitar erros
    pass

async def main():
    # Conectando à OLT Huawei via Telnet
    reader, writer = await telnetlib3.open_connection(
        host, port=port, shell=shell
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
    await executar_comando(writer, reader, "enable")
    await executar_comando(writer, reader, "config")
    await executar_comando(writer, reader, "display ont autofind all", delay=3)
    writer.write(" \n")

    # Listar interfaces antes de provisionar
    await listar_interfaces(writer, reader)

    # Dados de provisionamento
    slot_value = input("Informe o valor do campo SLOT: ")
    pon_value = input("Informe o valor do campo PON: ")
    id_value = input("Informe o valor do campo ID SERIAL: ")
    veip_value = input("Informe o valor do campo VEIP 30,300 ou 40,1022: ")
    vlan_value = input("Informe o valor do campo VLAN: ")
    desc_value = input("Informe o valor do campo DESCRIÇÃO: ")

    # Execução dos comandos de provisionamento
    await executar_comando(writer, reader, f"interface gpon 0/{slot_value}")
    # Executar o comando e capturar o resultado para aplicar o ID da ONU
    await executar_comando(writer, reader, f"ont confirm {pon_value} sn-auth {id_value} omci ont-lineprofile-id {veip_value} ont-srvprofile-id {vlan_value} desc {desc_value}", delay=2)
    writer.write("\n")  # Enviar um enter após o comando
    await writer.drain()
    await asyncio.sleep(1)  # Aumentar o tempo de espera
    output = await reader.read(4096)  # Aumentar o buffer de leitura
    print("Resultado do comando 'ont confirm':")
    print(output)
    onu_value = input("Informe o valor do campo ID ONU: ")
    writer.write("\n")  # Enviar um enter após o comando
    await executar_comando(writer, reader, f"ont port native-vlan {pon_value} {onu_value} eth 1 vlan {vlan_value}", delay=2)
    writer.write("\n")  # Enviar um enter após o comando
    await writer.drain()
    await asyncio.sleep(1)  # Aumentar o tempo de espera
    await executar_comando(writer, reader, "quit")
    writer.write("\n")  # Enviar um enter após o comando
    await writer.drain()
    await asyncio.sleep(1)  # Aumentar o tempo de espera
    await executar_comando(writer, reader, f"service-port vlan {vlan_value} gpon 0/{slot_value}/{pon_value} ont {onu_value} gemport 5 multi-service user-vlan {vlan_value}", delay=2)
    writer.write("\n")  # Enviar um enter após o comando
    await asyncio.sleep(1)  # Aumentar o tempo de espera

    # Executar o comando para leitura de potência e capturar o resultado
    await executar_comando(writer, reader, f"interface gpon 0/{slot_value}")
    await executar_comando(writer, reader, f"display ont optical-info {pon_value} {onu_value}", delay=10)
    writer.write("\n")  # Enviar um enter após o comando
    await writer.drain()
    await asyncio.sleep(3)  # Aumentar o tempo de espera
    output = await reader.read(4096)  # Aumentar o buffer de leitura
    print("Resultado da leitura de potência:")
    print(output)

    print("Provisionamento concluído 😎 ✅ ✅ ✅ ")

    # Fechando a conexão Telnet
    writer.close()

# Executar o script asyncio
asyncio.run(main())