import ipaddress

def calcular_subnet(ip, subnet):
    rede = ipaddress.IPv4Network(f'{ip}/{subnet}', strict=False)
    return rede

def main():
    ip = input("Digite o endereço IP (ex: 192.168.0.1): ")
    subnet = input("Digite a subnet (ex: /24): ")

    try:
        rede = calcular_subnet(ip, subnet)
        print(f'Endereço de Rede: {rede.network_address}')
        print(f'Endereço de Broadcast: {rede.broadcast_address}')
        print(f'Número total de hosts: {rede.num_addresses}')
    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
