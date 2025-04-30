import telnetlib3
import asyncio

async def main():
    # Solicitar ao usuário que insira as informações de login 🔑
    usuario = input("Insira o nome de usuário da OLT: ")
    senha = input("Insira a senha da OLT: ")
    port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"

    # Endereços IP e seus respectivos nomes pré-definidos da OLT Intelbras
    enderecos_ip = {
        "🖥  OLT INTELBRAS PARAISO": "172.31.188.2",
        "🖥  OLT INTELBRAS BOM_VIVER ➡": "172.31.248.2",
        "🖥  OLT INTELBRAS FORTALEZA ➡": "172.31.194.2",
        "🖥  OLT INTELBRAS 3 FUROS ➡": "172.31.195.2"
    }

    # Mostra os endereços IP disponíveis
    print("Endereços IP disponíveis:")
    for i, (nome, ip) in enumerate(enderecos_ip.items()):
        print(f"{i+1}. {nome} ({ip})")

    # Solicitar ao usuário que escolha um endereço IP
    escolha = int(input("Escolha um número de endereço IP: "))
    if escolha < 1 or escolha > len(enderecos_ip):
        print("Escolha inválida. Saindo do script.")
        return

    # Selecionar o endereço IP escolhido
    host = list(enderecos_ip.values())[escolha - 1]

    # Conectando à OLT Intelbras via Telnet
    reader, writer = await telnetlib3.open_connection(host, port)
    try:
        # Fazendo login
        writer.write(usuario + "\n")
        writer.write(senha + "\n")

        # Executando o comando "show ont-find list interface gpon all"
        writer.write("enable\n")
        writer.write("configure terminal\n")
        writer.write("show ont-find list interface gpon all\n")
        await asyncio.sleep(3)

        output = await reader.read(65536)
        print("Saída do comando 'show ont-find list interface gpon all':")
        print(output)

        # Função para executar comandos e mostrar saída
        async def executar_comando(writer, reader, comando):
            writer.write(comando + "\n")
            await asyncio.sleep(3)
            output = await reader.read(65536)
            print(output)

        # Dados de provisionamento
        sn_value = input("Informe o valor do campo ID Serial: ")

        # Executando o comando "show ont brief sn string-hex"
        await asyncio.sleep(1)
        writer.write(f"show ont brief sn string-hex {sn_value}\n")
        await asyncio.sleep(3)
        output = await reader.read(65536)
        print("show ont brief sn string-hex':")
        print(output)

        # Dados dos comandos de provisionamento
        pon_value = input("Informe o valor do campo PON: ")
        id_value = input("Informe o valor do campo ID: ")
        desc_value = input("Informe o valor do campo Nome: ")
        veip_value = input("Informe o valor do campo VEIP: ")

        # Execução dos comandos de provisionamento
        await executar_comando(writer, reader, f"interface gpon 0/{pon_value}")
        await executar_comando(writer, reader, "deploy profile rule")
        await executar_comando(writer, reader, f"aim 0/{pon_value}/{id_value} name {desc_value}")
        await executar_comando(writer, reader, f"permit sn string-hex {sn_value} line {veip_value} default line {veip_value}")
        await executar_comando(writer, reader, "active")
        await executar_comando(writer, reader, "y")
        await executar_comando(writer, reader, "exit")
        await executar_comando(writer, reader, "end")

        # Executar o comando "show ont optical-info"
        await asyncio.sleep(1)
        writer.write(f"show ont optical-info 0/{pon_value}/{id_value}\n")
        await asyncio.sleep(3)
        output = await reader.read(65536)
        print(output)
    finally:
        writer.close()
        await writer.wait_closed()

    print("Provisionamento concluído 😎 ✅ ✅ ✅ ")

# Executar o script principal
if __name__ == "__main__":
    asyncio.run(main())
