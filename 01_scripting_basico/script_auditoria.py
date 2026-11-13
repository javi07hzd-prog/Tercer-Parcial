import requests
import json
from requests.auth import HTTPBasicAuth

# Deshabilitar advertencias de certificados SSL autofirmados
requests.packages.urllib3.disable_warnings()

# 1. Parámetros de la API RESTCONF
url = "https://192.168.1.1/restconf/data/ietf-interfaces:interfaces"
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
auth = HTTPBasicAuth("admin", "C1scoPassword12345!")
lista_interfaces = []

try:
    # 2. Petición GET HTTP
    response = requests.get(
        url,
        headers=headers,
        auth=auth,
        verify=False, 
        timeout=10
    )
    # 3. Validación del código de respuesta
    if response.status_code == 200:
        data = response.json()
        interfaces = data["ietf-interfaces:interfaces"]["interface"]
        print(f"{'Nombre':<25} {'IP':<18} {'Habilitada':<10}")
        print("-" * 55)
        for interface in interfaces:
            name = interface.get("name", "N/A")
            enabled = interface.get("enabled", False)
            ipv4 = interface.get("ietf-ip:ipv4", {})
            direcciones = ipv4.get("address", [])
            if enabled == True and len(direcciones) > 0:
                ip = direcciones[0].get("ip", "N/A")
                print(f"{name:<25} {ip:<18} {str(enabled):<10}")
                interfaz = {
                    "interfaz": name,
                    "ip": ip,
                    "habilitada": enabled
                }
                lista_interfaces.append(interfaz)
        archivo = open("inventario_interfaces.json", "w")
        json.dump(lista_interfaces, archivo, indent=4)
        archivo.close()
        print("Datos guardados en inventario_interfaces.json")
    else:
        print(f"Error HTTP {response.status_code}: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")