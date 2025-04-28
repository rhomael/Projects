import telnetlib3
import asyncio
import re
import time

# Solicitar ao usuário que insira as informações de login 🔑
usuario = input("Insira o nome de usuário da OLT: ")
senha = input("Insira a senha da OLT: ")
port = input("Insira a porta de acesso da OLT (default: 23): ") or "23"
senha_enable = input("Insira a senha enable da OLT: ")

# Endereços IP e seus respectivos nomes pré-definidos da OLT Fiberhome
enderecos_ip = {
    "🖥  OLT PINHEIRO ➡": "172.31.255.3",
    "🖥  OLT SÃO LUIS ➡": "172.30.247.100",
    "🖥  OLT SAO BENTO ➡": "172.31.254.2",
    "🖥  OLT TURIACU ➡": "172.31.200.254",
    "🖥  OLT VILA DA PAZ ➡": "172.31.187.2",
    "🖥  OLT SANTA HELENA ➡": "172.30.253.254",
    "🖥  OLT PEDRO DO ROSARIO ➡": "172.31.246.2",
    "🖥  OLT PACAS ➡": "172.31.191.2",
    "🖥  OLT PRESIDENTE SARNEY ➡": "172.31.252.3",
    "🖥  OLT CONECTA ➡": "177.66.195.157",
    "🖥  OLT SLP ➡": "172.31.254.2",
    "🖥  OLT MHZ ➡": "172.16.0.2",
    "🖥  OLT GNF ➡": "172.31.253.2"
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

# Comandos de provisionamento
comandos_provisionamento = [
    "set whitelist phy_addr address {0} password null action delete\n",
    "set whitelist phy_addr address {0} password null action add slot {1} pon {2} onu {3} type HG260",
    "cd lan",
    "set epon slot {1} pon {2} onu {3} port 1 service number 1",
    "set epon slot {1} pon {2} onu {3} port 1 service 1 vlan_mode {6} {7} 33024 {4}",
    "set epon slot {1} pon {2} onu {3} port 1 onuveip 1 33024 {4} 65535 33024 65535 65535 33024 65535 65535 0 {5} 65535 servn null service_type 1",
    "apply onu {1} {2} {3} vlan",
    "cd .."
]

async def telnet_session():
    reader, writer = await telnetlib3.open_connection(host, port, shell=None)
    try:
        # Fazendo login
        await reader.readuntil(b"Login: ")  # Convertendo para bytes
        writer.write(usuario + "\n")
        await reader.readuntil(b"Password: ")  # Convertendo para bytes
        writer.write(senha + "\n")

        # Habilitando o modo privilegiado
        writer.write("enable\n")
        await reader.readuntil(b"Password: ")  # Convertendo para bytes
        writer.write(senha_enable + "\n")

        # Executando o comando "show discovery slot all pon all"
        writer.write("cd onu\n")
        writer.write("show discovery slot all pon all\n")
        await asyncio.sleep(15)
        output = await reader.read(65535)
        print(output)

        # Atualizando os campos em Dados de provisionamento
        id_value = input("Informe o valor do campo ID: ")
        slot_value = input("Informe o valor do campo SLOT: ")
        pon_value = input("Informe o valor do campo PON: ")
        vlan_value = input("Informe o valor do campo VLAN: ")
        veip_value = input("Informe o valor do campo VEIP 1 ou 2: ")
        vlan_mode = input("Informe o valor do campo TAG ou TRANSPARENT: ")
        id_vlan_mode = input("Informe o valor do campo ID VLAN 0 ou 255: ")

        # Executar o comando "set whitelist delete"
        writer.write(f"set whitelist phy_addr address {id_value} password null action delete\n")
        await asyncio.sleep(1)
        output = await reader.read(65535)

        # Executar o comando "show authorization"
        writer.write(f"show authorization slot {slot_value} pon {pon_value}\n")
        await asyncio.sleep(1)
        output = await reader.read(65535)

        # Executando o comando vazio até a mensagem "Command execute success."
        timeout = 100
        start_time = time.time()
        while "Command execute success." not in output:
            writer.write("\n")
            await asyncio.sleep(0.5)
            output += await reader.read(65535)
            if time.time() - start_time > timeout:
                print("Timeout atingido. Não foi possível obter a mensagem 'Command execute success.'")
                break

        # Extrair números da coluna
        numbers = re.findall(r"\b(\d{1,3})\b", output)

        # Encontrar o próximo número pulado
        if numbers:
            numbers = list(map(int, numbers))
            min_number = min(numbers)
            max_number = max(numbers)
            sequence = list(range(min_number, max_number + 1))
            missing_numbers = list(set(sequence) - set(numbers))
            if missing_numbers:
                onu_value = str(min(missing_numbers))
            else:
                onu_value = str(max_number + 1)
        else:
            onu_value = "1"

        # Executando os comandos de provisionamento
        for comando_provisionamento in comandos_provisionamento:
            comando_provisionamento = comando_provisionamento.format(
                id_value, slot_value, pon_value, onu_value, vlan_value, veip_value, vlan_mode, id_vlan_mode
            )
            writer.write(comando_provisionamento + "\n")
            await asyncio.sleep(1.5)
            output = await reader.read(65535)
            print(output)

        # Executar o comando "show optic_module slot pon onu"
        await asyncio.sleep(5)
        writer.write(f"show optic_module slot {slot_value} pon {pon_value} onu {onu_value}\n")
        await asyncio.sleep(10)
        output = await reader.read(65535)
        print(output)
    finally:
        writer.close()

# Iniciar a sessão Telnet
asyncio.run(telnet_session())
