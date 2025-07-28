import os
import re
import pandas as pd

from datetime import datetime
from app.users import get_users


EXCEL_PATH = "app/192.168.0.52/ti/SISGIA/Gestión de Tickets/Bitácora de desarrollo/"


def guardar_en_excel(data):
    """Guarda los datos del commit en un archivo Excel."""

    # Obtener el mensaje del commit
    mensaje = data["head_commit"]["message"]

    # Identificar el ticket y la descripción
    regex = re.search(r"^(\[[\d-]*\]\s[A-Za-z\.\d]*)\s-\s([\w\W]+)$", mensaje)

    ticket = regex.group(1)
    descripcion_split = (regex.group(2)).split("-")

    # Extraer el campo tarea y la acción tomada
    campo_tarea = "-".join(descripcion_split[:-1])
    campo_accion_tomada = descripcion_split[-1].strip()

    # Obtener el usuario del commit y construir la ruta del archivo Excel
    user = get_users()[data["head_commit"]["committer"]["username"]]

    excel_route = os.path.join(
        EXCEL_PATH, user, f"2025 - Bitácora de desarrollo - {user}.xlsx"
    )

    print(f"Guardando en la ruta: {excel_route}")

    # Cargar el archivo Excel
    df = pd.read_excel(excel_route, sheet_name=1)
    print(df)

    # Verificar si el ticket ya existe en el archivo Excel
    ticket_exists = df[df["Ticket - Proyectos"] == ticket]

    # Si el ticket no existe, asignar un nuevo hash y fecha de asignación
    if ticket_exists.empty:
        hash = max(df["Hash"].values) + 1 if not df.empty else 1
        fecha_asignacion = datetime.strptime(ticket[1:11], "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
    else:
        hash = ticket_exists["Hash"].values[0]
        fecha_asignacion = ticket_exists["Fecha de asignación"].values[-1]

    fecha_resolucion = datetime.strptime(
        data["head_commit"]["timestamp"], "%Y-%m-%dT%H:%M:%S%z"
    ).strftime("%d/%m/%Y")
    estado = "Terminado"

    nueva_fila = {
        "Ticket - Proyectos": ticket,
        "Hash": hash,
        "Tarea": campo_tarea,
        "Fecha de asignación": fecha_asignacion,
        "Fecha de Resolución": fecha_resolucion,
        "Acción Tomada": campo_accion_tomada,
        "Estado": estado,
        "Notas": "",
    }
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    print(df)

    with pd.ExcelWriter(
        excel_route, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        df.to_excel(writer, sheet_name=writer.book.sheetnames[1], index=False)
    return
