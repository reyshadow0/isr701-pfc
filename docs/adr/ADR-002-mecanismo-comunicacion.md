# ADR-002: Mecanismo de comunicación principal

- **Estado:** Aceptado
- **Fecha:** 21 de noviembre de 2026
- **Autores:** Mario Castro (Líder de Desarrollo)

## Contexto

El ADR-001 dividió el sistema en cinco servicios. Casi todo lo que pasa entre ellos puede esperar unos segundos y va por eventos, pero hay un caso que no: antes de abrir la rúbrica, Evaluación y actas tiene que saber si el estudiante ya subió el informe y el reporte de URKUND, y cuál es el porcentaje de coincidencia. Ese dato es de Solicitudes y documentos. Evaluación no puede usar una copia vieja, porque el porcentaje es PC/EC en la sección 9: si no se puede confirmar, la rúbrica no se abre.

Entonces la llamada de Evaluación a Solicitudes es síncrona. Evaluación pregunta, espera y con la respuesta decide si deja calificar. Lo que falta decidir es con qué mecanismo se hace esa llamada.

La guía del PFC pide justificar esta elección con lo que medimos en PE-U1. En esa práctica comparamos sockets TCP y gRPC con el mismo intercambio: tres nodos en procesos separados de una sola máquina, en localhost y sin Docker, con Python 3.13 y `grpcio` 1.85.3. Cada nodo enviaba un mensaje y esperaba un acuse.

Hay otras dos comunicaciones que este ADR no compara porque las fija otra cosa. Entre la aplicación web y el API Gateway, y del gateway a cada servicio, va REST con JSON, porque es lo que habla el navegador. Los avisos y cambios de estado van por eventos en RabbitMQ (AMQP), porque quien los envía no tiene que esperar. El detalle de cada interacción está en la sección 8 del documento.

## Opciones consideradas

1. **Sockets TCP.** Es lo que se programó en `src/sockets/` de PE-U1: una conexión por destino y cada mensaje como un objeto JSON que termina en salto de línea.
   - A favor: no necesita librerías aparte y, en principio, agrega menos capas entre los dos procesos.
   - En contra: el formato del mensaje lo inventamos nosotros. El servidor tuvo que revisar a mano que llegara la línea completa, que `sender` fuera texto y que `timestamp` fuera un entero no negativo. También tuvimos que escribir los tiempos de espera, los reintentos y las respuestas de error. Si un servicio cambia un campo y el otro no, el error recién aparece cuando el sistema está corriendo.
2. **gRPC.** Es lo que se programó en `src/grpc/` de PE-U1: el servicio y sus mensajes se definen en un archivo `.proto` y `grpcio-tools` genera el código del cliente y del servidor.
   - A favor: el contrato está escrito en un solo archivo que comparten los dos servicios. Los tipos los revisa el código generado. El tiempo máximo de espera es un parámetro de la llamada, y cuando falla, el cliente recibe un código claro (`UNAVAILABLE`, `DEADLINE_EXCEEDED`).
   - En contra: es una dependencia más y hay que volver a generar el código cada vez que cambia el `.proto`. Además, no se puede probar desde el navegador ni con `curl`.

## Decisión

Elegimos **gRPC** para las llamadas directas entre servicios. Por ahora hay una sola: Evaluación y actas le pregunta a Solicitudes y documentos por una solicitud.

En la corrida oficial de PE-U1 del **[PENDIENTE: fecha de la corrida]**, en **[PENDIENTE: equipo y procesador]**, la latencia de ida y vuelta fue de **[PENDIENTE] ms** con sockets TCP y de **[PENDIENTE] ms** con gRPC (mediana de **[PENDIENTE]** mensajes). **[PENDIENTE: escribir aquí lo que muestran las cifras. Si gRPC salió más lento, decir cuánto y por qué no pesa en este sistema; si salió igual o más rápido, decirlo así.]**

Lo que más pesó fue el contrato. El sistema tiene pocas decenas de usuarios a la vez (RNF-01), así que unos milisegundos de diferencia no los nota nadie, pero un campo mal leído entre Evaluación y Solicitudes sí: es justo el dato que decide si el tribunal puede calificar. Con gRPC ese contrato queda en `src/proto/solicitudes.proto` y no en la cabeza de cada integrante.

Lo que se sabe de cómo trabaja el equipo también cuenta. En PE-U1 ya armamos un servidor y un cliente gRPC en Python y generamos el código con `grpcio-tools`, así que el esqueleto de E1 reusa ese mismo patrón.

## Consecuencias

- **Lo que ganamos:**
  - un solo contrato tipado para los dos servicios, que no depende del lenguaje en que estén escritos;
  - si Solicitudes no responde en 5 segundos, Evaluación recibe un error y no sigue, que es lo que pide la sección 9 para el porcentaje de URKUND;
  - el patrón ya lo probamos en PE-U1 y en el esqueleto.
- **Lo que cuesta:** hay más configuración que con TCP plano. Hay que instalar `grpcio` y `grpcio-tools`, generar el código, subirlo al repositorio y volver a generarlo cada vez que cambie el `.proto`. Para probar la llamada a mano no basta un navegador; hace falta un cliente gRPC.
- **Lo que hay que vigilar:**
  - Evaluación depende de que Solicitudes esté arriba. Si Solicitudes se cae, la rúbrica no se abre y el tribunal califica en papel, como hoy. Es una decisión a propósito (sección 9), pero hay que tenerla presente en E3 cuando haya réplicas.
  - Las llamadas van sin cifrar (`insecure_channel`) porque en E1 todo corre en la misma máquina. Cuando los servicios estén en contenedores separados (E2), hay que decidir si la red interna basta o si se agrega TLS.
  - Si en E2 los servicios pasan a Spring Boot, el mismo `.proto` sirve para generar el código en Java.
