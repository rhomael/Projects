import requests

def get_mac_vendor(mac_address):
    url = 'https://api.macvendors.com/'
    response = requests.get(url + mac_address)
    if response.status_code == 200:
        return response.text
    else:
        return 'Não foi possível obter o fabricante do MAC address ❌.'

# Solicitar o MAC Address ao usuário
mac_address = input("Digite o MAC Address que deseja verificar: ")

fabricante = get_mac_vendor(mac_address)
print(f'Fabricante do MAC address ➡ {mac_address}: {fabricante}')
