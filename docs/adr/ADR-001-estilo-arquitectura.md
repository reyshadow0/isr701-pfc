# ADR-001: Estilo de arquitectura

- **Estado:** Aceptado
- **Fecha:** 20 de noviembre de 2026
- **Actualizado:** 21 de noviembre de 2026, con las dos aclaraciones de la revisión de coherencia de Jilmar Cedeño (issue #20)
- **Autores:** Dariem Benites (Arquitecto)

## Contexto

El sistema gestiona las predefensas de Titulación II en la UTEQ. Cubre:

- la entrega del informe y del reporte de URKUND;
- el cronograma con fecha, sala y tribunal;
- la calificación del tribunal con la rúbrica;
- la nota final (40 % del tribunal y 60 % del docente de Titulación II);
- el acta.

Hoy todo eso pasa por correo, papel, Word, Excel, URKUND y el SGA, sin un sistema que lo una. Así lo contó la entrevistada el 19 de noviembre de 2026.

Lo que pesa en la decisión:

- **Poca carga.** Cada período presentan de 10 a 12 estudiantes, cada uno con 2 o 3 PDF de hasta 20 MB, y en la semana 19 hay a lo mucho unas decenas de usuarios a la vez (RNF-01 y RNF-05). Blinowski et al. [1] encontraron que en una sola máquina un monolito rinde mejor que su versión en microservicios. También advierten que, para sistemas sin miles de usuarios simultáneos, los beneficios de migrar no están claros. Por eso el rendimiento no es lo que nos lleva a distribuir.
- **Partes que no pueden caer juntas.** En la semana de predefensas, las funciones críticas no pueden pasar más de 60 minutos seguidos sin servicio (RNF-02). Si fallan los avisos o el cronograma, el tribunal tiene que poder seguir calificando en el sistema. Si falla la validación de documentos, la predefensa sigue y las notas se registran después.
- **Datos con necesidades distintas.** Las notas, el acta, el porcentaje de URKUND y la asignación de fecha, sala y tribunal tienen que estar siempre exactos. Los avisos por correo, el estado visible y los reportes pueden tardar un poco.
- **El curso.** En E2 el sistema se divide en microservicios con API y contenedores, y en E3 se distribuye la base de datos. Lo que decidamos aquí tiene que servir para esas entregas.
- **El equipo.** Somos cuatro y trabajamos en paralelo, cada uno en su rama.
- **Un antecedente.** PresustentacionesAWPS, un sistema anterior para el mismo proceso, es un monolito: un backend Spring Boot, una base PostgreSQL y los PDF en el disco del servidor. En la FORM-AC-01 ya lo marcamos como un punto único de falla.

## Opciones consideradas

1. **Monolito.** Una aplicación Spring Boot con una base PostgreSQL en un servidor.
   - A favor: es lo más simple de programar, probar y desplegar, y con esta carga rinde bien.
   - En contra:
     - si se cae, se cae todo a la vez: la entrega, el cronograma y las notas;
     - cualquier cambio obliga a desplegar la aplicación completa, también en la semana de predefensas;
     - toda la base sigue la misma política de consistencia;
     - no sirve para E2 ni para E3.
2. **Monolito modular.** Una sola aplicación, con un módulo por cada parte del proceso.
   - A favor: ordena el código por dominio sin llamadas por la red.
   - En contra: sigue siendo un solo proceso con una sola base. Si un módulo falla, arrastra a los demás, y no se pueden desplegar por separado.
3. **Microservicios por dominio.** Un servicio por cada parte del proceso, cada uno con su base, una sola entrada por un API Gateway y eventos por una cola de mensajes.
   - A favor:
     - cada servicio falla y se despliega por separado;
     - cada dato tiene la política que necesita;
     - cada integrante trabaja en un servicio sin chocar con los demás;
     - es lo que piden E2 y E3.
   - En contra: hay más piezas que instalar y vigilar, las llamadas por la red pueden fallar o tardar, y lo que viaja por la cola llega con algo de retraso.

## Decisión

Elegimos **microservicios por dominio** (opción 3), como muestra el diagrama C4 de nivel 2 (`docs/diagramas/c4-nivel2-contenedores.png`):

- **Cinco servicios:** Usuarios, Cronograma, Solicitudes y documentos, Evaluación y actas, y Notificaciones. Los separamos según quién hace cada cosa y en qué momento del proceso, como lo contó la entrevistada.
- **Una base por servicio.** Ningún servicio lee la base de otro: le pregunta al servicio o recibe un evento. Los PDF van en un almacén de archivos (MinIO), fuera de la base.
- **Notas y acta en el mismo servicio** (Evaluación y actas), para que nunca se genere un acta con una nota que no está registrada. Evaluación y actas solo genera el acta si puede confirmar en su base primaria la nota vigente de cada miembro del tribunal. Si no puede confirmarla, no genera el acta hasta que pueda hacerlo. Así respondemos al riesgo R02, con la misma regla de la sección 09.
- **Una sola entrada.** La aplicación web habla con el API Gateway, que valida el JWT y envía cada petición al servicio que corresponde.
- **Una instancia por servicio en E1.** Alcanza para unas decenas de usuarios; las réplicas llegan en E3.

El ADR-002 decide qué servicios se llaman directamente, cuáles se avisan por eventos y con qué mecanismo.

## Consecuencias

- **Lo que ganamos:**
  - si se caen Notificaciones o Cronograma, el tribunal sigue calificando, y eso ayuda a cumplir RNF-02 en la semana de predefensas;
  - las notas son exactas porque un solo servicio las escribe;
  - cada integrante tiene una parte clara del código.
- **Lo que cuesta:** hay que levantar el gateway, la cola, MinIO y cinco bases, que en E2 van en contenedores. Los servicios necesitan contratos claros entre sí (OpenAPI y archivos `.proto`) y más pruebas de integración.
- **Lo que hay que vigilar:**
  - Si Solicitudes y documentos está caído, Evaluación y actas no puede confirmar el informe ni el porcentaje de URKUND, y la rúbrica digital queda bloqueada. El tribunal sigue con la predefensa, califica en papel y registra las notas cuando vuelve el servicio, como se describe en la sección 08. Por eso RNF-02 pide recuperar las funciones críticas en 60 minutos como máximo.
  - Con una sola instancia, el API Gateway es un punto único de falla: si se cae, nadie entra. Es el riesgo R03 y se revisa en E3.
  - El estado visible y los avisos pueden tardar unos segundos, porque llegan por eventos. La entrevistada dijo que eso es aceptable.
  - El mecanismo de las llamadas directas se elige con lo medido en PE-U1, en el ADR-002.

## Referencias

[1] G. Blinowski, A. Ojdowska y A. Przybyłek, "Monolithic vs. microservice architecture: A performance and scalability evaluation," *IEEE Access*, vol. 10, pp. 20357–20374, 2022, doi: 10.1109/ACCESS.2022.3152803.
