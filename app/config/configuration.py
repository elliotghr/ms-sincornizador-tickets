import os


def get_config():
    """Obtiene la configuración del servidor y las credenciales."""
    return {
        "excel_route": "//192.168.0.52/ti",
        "sub_path": "SISGIA/Gestión de Tickets/Bitácora de desarrollo/",
        "server_user": os.getenv("server_user"),
        "password": os.getenv("password"),
    }
