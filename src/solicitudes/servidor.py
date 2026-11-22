"""Servicio Solicitudes y documentos (esqueleto de E1).

Expone ConsultarSolicitud por gRPC y responde siempre con datos fijos.
La base de datos, MinIO y las reglas del trámite llegan en E2.

Uso, desde la raíz del repositorio:
    python -m src.solicitudes.servidor
    python -m src.solicitudes.servidor --puerto 50051
"""

import argparse
from concurrent import futures
from datetime import datetime

import grpc

from src.proto import solicitudes_pb2
from src.proto import solicitudes_pb2_grpc


class SolicitudesServicer(solicitudes_pb2_grpc.SolicitudesServiceServicer):

    def ConsultarSolicitud(self, request, context):
        hora = datetime.now().strftime("%H:%M:%S")
        print(f"[Solicitudes {hora}] Consulta recibida: {request.id_solicitud}")

        # Respuesta fija: en el esqueleto no hay base de datos.
        return solicitudes_pb2.DatosSolicitud(
            id_solicitud=request.id_solicitud,
            estado="ENVIADA",
            informe_cargado=True,
            reporte_urkund_cargado=True,
            porcentaje_urkund=4.5,
        )


def iniciar_servidor(host, puerto):
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    solicitudes_pb2_grpc.add_SolicitudesServiceServicer_to_server(
        SolicitudesServicer(), servidor
    )

    servidor.add_insecure_port(f"{host}:{puerto}")
    servidor.start()
    print(f"[Solicitudes] Servidor gRPC escuchando en {host}:{puerto}")
    print("[Solicitudes] Ctrl+C para detenerlo")

    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Solicitudes] Deteniendo el servidor")
        servidor.stop(0).wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servicio Solicitudes y documentos")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--puerto", type=int, default=50051)
    args = parser.parse_args()

    iniciar_servidor(args.host, args.puerto)
