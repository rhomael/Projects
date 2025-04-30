import telnetlib3
import asyncio

async def main():
    # Solicitar ao usuário que insira as informações de login 🔑
    usuario = input("Insira o nome de usuário da OLT: ")
    senha = input("Insira a senha da OLT: ")
    port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"

    # Endereços IP e seus respectivos nomes pré-definidos da OLT ZTE
    enderecos_ip = {
        "🖥  OLT ZTE PARAISO ➡": "172.31.188.2",
        "🖥  OLT ZTE PALMEIRANDIA ➡": "172.31.239.2"
    }

    # Mostrar os endereços IP disponíveis
    print("Endereços IP disponíveis: ")
    for i, (nome, ip) in enumerate(enderecos_ip.items()):
        print(f"{i + 1}. {nome} ({ip})")

    # Solicitar ao usuário que escolha um endereço IP
    escolha = int(input("Escolha um número de endereço IP: "))
    if escolha < 1 or escolha > len(enderecos_ip):
        print("Escolha inválida. Saindo do script")
        return

    # Selecionar o endereço IP escolhido
    host = list(enderecos_ip.values())[escolha - 1]

    # Conectando à OLT ZTE via telnet
    reader, writer = await telnetlib3.open_connection(host, port)
    try:
        # Função para leitura com timeout
        async def ler_com_timeout(reader, timeout=5):
            try:
                return await asyncio.wait_for(reader.read(), timeout=timeout)
            except asyncio.TimeoutError:
                print("[ERRO] Timeout ao aguardar resposta do servidor.")
                return ""

        # Fazendo login
        await asyncio.sleep(0.5)
        writer.write(usuario + "\n")
        await asyncio.sleep(0.5)
        writer.write(senha + "\n")
        await asyncio.sleep(0.5)

        # Executando o comando "show pon onu uncfg"
        await asyncio.sleep(0.5)
        writer.write("configure terminal\n")
        await asyncio.sleep(0.5)
        writer.write("show pon onu uncfg\n")
        output = await ler_com_timeout(reader, timeout=10)
        print("Saída do comando 'show pon onu uncfg':")
        print(output)

        # Dados de PON
        pon_value = input("Informe o valor do campo PON: ")

        # Executar o comando "show gpon onu state"
        writer.write(f"show gpon onu state gpon_olt-1/3/{pon_value}\n")
        output = await ler_com_timeout(reader, timeout=10)
        print("Saída do comando 'show gpon onu state':")
        print(output)

        # Função para executar comandos e mostrar saída
        async def executar_comando(writer, reader, comando, timeout=5):
            writer.write(comando + "\n")
            await asyncio.sleep(1)
            output = await ler_com_timeout(reader, timeout=timeout)
            print(output)

        # Dados de Provisionamento
        id_onu = input("Informe o valo do campo ID ONU: ")
        type_onu = input("Informe o campo type ZTE-F643 ou ZTE-F660: ")
        sn_onu = input("Informe o campo da SERIAL: ")
        vlan_value = input("Informe o campo da VLAN: ")
        name_onu = input("Informe o nome do CLIENTE: ")

        # Executando comandos de Provisionamento
        await executar_comando(writer, reader, '!')
        await executar_comando(writer, reader, f"interface gpon_olt-1/3/{pon_value}")
        await executar_comando(writer, reader, f"onu {id_onu} type {type_onu} sn {sn_onu}")
        await executar_comando(writer, reader, "exit")
        await executar_comando(writer, reader, "!")
        await executar_comando(writer, reader, f"interface gpon_onu-1/3/{pon_value}:{id_onu}")
        await executar_comando(writer, reader, f"name {name_onu}")
        await executar_comando(writer, reader, f"sn-bind enable sn")
        await executar_comando(writer, reader, f"tcont 4 profile 1G")
        await executar_comando(writer, reader, f"gemport 1 tcont 4")
        await executar_comando(writer, reader, "exit")
        await executar_comando(writer, reader, "!")
        await executar_comando(writer, reader, f"interface vport-1/3/{pon_value}.{id_onu}:1")
        await executar_comando(writer, reader, f"service-port 1 user-vlan {vlan_value} vlan {vlan_value}")
        await executar_comando(writer, reader, "exit")
        await executar_comando(writer, reader, "!")
        await executar_comando(writer, reader, f"pon-onu-mng gpon_onu-1/3/{pon_value}:{id_onu}")
        await executar_comando(writer, reader, f"service 1 gemport 1 vlan {vlan_value}")
        await executar_comando(writer, reader, f"vlan port eth_0/1 mode tag vlan {vlan_value}")
        await executar_comando(writer, reader, "exit")
        await executar_comando(writer, reader, "exit")

        # Executar o comando "show pon power attenuation"
        writer.write(f"show pon power attenuation gpon_onu-1/3/{pon_value}:{id_onu}\n")
        output = await ler_com_timeout(reader, timeout=10)
        print(output)

    finally:
        writer.close()

    print("Provisionamento concluído 😎 ✅ ✅ ✅ ")

if __name__ == "__main__":
    asyncio.run(main())
