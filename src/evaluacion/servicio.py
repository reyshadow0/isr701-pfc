"""Servicio Evaluación y actas (esqueleto de E1).

Al arrancar le pregunta a Solicitudes por una solicitud usando gRPC
(el mecanismo del ADR-002) y muestra la respuesta en la consola.
La rúbrica, las notas y el acta llegan en E2.

Uso, desde la raíz del repositorio:
    python -m src.evaluacion.servicio
    python -m src.evaluacion.servicio --solicitud SOL-2026-002 --destino 127.0.0.1:50051
"""

import argparse
import sys

import grpc

from src.proto import solicitudes_pb2
from src.proto import solicitudes_pb2_grpc

TIEMPO_MAXIMO = 5  # segundos que se espera la respuesta de Solicitudes


def consultar_solicitud(destino, id_solicitud):
    print(f"[Evaluación] Consultando la solicitud {id_solicitud} en {destino}")

    with grpc.insecure_channel(destino) as canal:
        stub = solicitudes_pb2_grpc.SolicitudesServiceStub(canal)
        consulta = solicitudes_pb2.ConsultaSolicitud(id_solicitud=id_solicitud)

        try:
            datos = stub.ConsultarSolicitud(consulta, timeout=TIEMPO_MAXIMO)
        except grpc.RpcError as error:
            # Sin respuesta de Solicitudes no se sigue: no hay un dato confirmado.
            print(f"[Evaluación] Solicitudes no respondió: {error.code().name}")
            return False

    print("[Evaluación] Respuesta de Solicitudes:")
    print(f"  Solicitud:          {datos.id_solicitud}")
    print(f"  Estado:             {datos.estado}")
    print(f"  Informe cargado:    {'sí' if datos.informe_cargado else 'no'}")
    print(f"  Reporte de URKUND:  {'sí' if datos.reporte_urkund_cargado else 'no'}")
    print(f"  Coincidencia:       {datos.porcentaje_urkund} %")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servicio Evaluación y actas")
    parser.add_argument("--destino", default="127.0.0.1:50051",
                        help="host:puerto del servicio Solicitudes")
    parser.add_argument("--solicitud", default="SOL-2026-001",
                        help="identificador de la solicitud a consultar")
    args = parser.parse_args()

    ok = consultar_solicitud(args.destino, args.solicitud)
    sys.exit(0 if ok else 1)
