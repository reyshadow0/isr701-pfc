# Sistema de gestión de documentos de pre-sustentaciones de trabajos de titulación

Proyecto Fin de Curso (PFC) de Aplicaciones Distribuidas (ISR-701) · Universidad Técnica Estatal de Quevedo ·
Séptimo nivel, paralelo B · SPA 2026–2027 · Docente: Gleiston Cicerón Guerrero Ulloa, PhD

Este repositorio se usa en las cuatro entregas del PFC: E1 (definición, requisitos y arquitectura base),
E2 (microservicios, API y contenedores), E3 (base de datos distribuida y procesamiento) y E4 (sistema final
y defensa).

## Integrantes y roles (equipo BCCP)

| Integrante | Rol | GitHub |
|---|---|---|
| Benites Pérez Dariem Alberto | Arquitecto | [@DALBEZ-ROG](https://github.com/DALBEZ-ROG) |
| Castro Coello Mario Sebastián | Líder de Desarrollo | [@reyshadow0](https://github.com/reyshadow0) |
| Cedeño Intriago Jilmar Jesús | Responsable de Calidad | [@jcedenoi4](https://github.com/jcedenoi4) |
| Pozo Castillo Steven Fernando | Responsable de Documentación | [@Redsito1215](https://github.com/Redsito1215) |

## Estructura del repositorio

| Ruta | Contenido |
|---|---|
| `src/proto/` | Contrato gRPC (`solicitudes.proto`) y el código generado a partir de él |
| `src/solicitudes/` | Servicio Solicitudes y documentos (servidor gRPC) |
| `src/evaluacion/` | Servicio Evaluación y actas (consulta a Solicitudes por gRPC) |
| `requirements.txt` | Paquetes de Python del esqueleto, con versión fija |
| `docs/main.tex` | Archivo principal del documento |
| `docs/secciones/` | Una sección del documento por archivo |
| `docs/referencias.bib` | Referencias (BibLaTeX, estilo IEEE) |
| `docs/figuras/` | Figuras del documento |
| `docs/diagramas/` | Diagramas C4 editables y sus exportaciones |
| `docs/adr/` | Registros de decisiones de arquitectura (ADR) |
| `docs/main.pdf` | Documento compilado |
| `evidencias/` | Levantamiento de información, fotografías de las sesiones y capturas del esqueleto |
| `BITACORA.md` | Bitácora de las sesiones de trabajo del equipo |

## Cómo ejecutar el esqueleto

El esqueleto de E1 tiene dos servicios que se hablan por gRPC, como decide el ADR-002.
Evaluación y actas le pregunta a Solicitudes y documentos por una solicitud, y Solicitudes responde con
datos fijos. Todavía no hay base de datos, inicio de sesión ni reglas del trámite: eso llega en E2.

### Requisitos

- Python 3.13 (se probó con 3.13.15). Revisa tu versión con `py --version` en Windows o
  `python3 --version` en Linux y macOS.
- Git, para clonar el repositorio.
- El puerto 50051 libre en tu máquina.

No hace falta generar el código de gRPC: los archivos `src/proto/solicitudes_pb2.py` y
`src/proto/solicitudes_pb2_grpc.py` ya vienen en el repositorio.

### 1. Clonar e instalar (una sola vez)

En PowerShell (Windows):

```powershell
git clone https://github.com/reyshadow0/isr701-pfc.git
cd isr701-pfc
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell no deja ejecutar `Activate.ps1`, corre primero
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` (solo afecta a esa ventana) y vuelve a
activar el entorno.

En Linux o macOS cambian dos líneas:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 2. Arrancar Solicitudes (terminal 1)

Todos los comandos se ejecutan desde la raíz del repositorio, con el entorno activado.

```powershell
python -m src.solicitudes.servidor
```

Si funcionó, se ve esto y la terminal se queda esperando:

```text
[Solicitudes] Servidor gRPC escuchando en 127.0.0.1:50051
[Solicitudes] Ctrl+C para detenerlo
```

### 3. Arrancar Evaluación (terminal 2)

Abre otra terminal, entra a la carpeta del repositorio, activa el entorno (`.\.venv\Scripts\Activate.ps1`) y
ejecuta:

```powershell
python -m src.evaluacion.servicio
```

Evaluación hace la consulta, muestra la respuesta y termina:

```text
[Evaluación] Consultando la solicitud SOL-2026-001 en 127.0.0.1:50051
[Evaluación] Respuesta de Solicitudes:
  Solicitud:          SOL-2026-001
  Estado:             ENVIADA
  Informe cargado:    sí
  Reporte de URKUND:  sí
  Coincidencia:       4.5 %
```

Al mismo tiempo, en la terminal 1 aparece la consulta recibida, con la hora:

```text
[Solicitudes 20:35:40] Consulta recibida: SOL-2026-001
```

Para consultar otra solicitud: `python -m src.evaluacion.servicio --solicitud SOL-2026-002`.

### 4. Qué pasa si Solicitudes está apagado

Detén Solicitudes con Ctrl+C y vuelve a ejecutar Evaluación. Como no hay un dato confirmado, Evaluación no
sigue y termina con código 1:

```text
[Evaluación] Solicitudes no respondió: UNAVAILABLE
```

### Si cambias el contrato

Después de editar `src/proto/solicitudes.proto`, vuelve a generar el código desde la raíz del repositorio y
sube los archivos generados junto con el `.proto`:

```powershell
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. src/proto/solicitudes.proto
```

[Video de demostración](https://youtu.be/9z9n4sfSKrc)

## Compilación del documento

- **Compilador:** `pdflatex`
- **Bibliografía:** `biber` (paquete `biblatex` con estilo `ieee`)
- **Archivo principal:** `docs/main.tex`
- **Distribución usada:** MiKTeX 26.5 en Windows

Orden de comandos, ejecutados dentro de la carpeta `docs/`:

```bash
cd docs
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

El resultado es `docs/main.pdf`.

### Dependencias

Paquetes de LaTeX: `fontenc`, `inputenc`, `babel` (idioma `spanish`), `lmodern`, `microtype`,
`geometry`, `graphicx`, `booktabs`, `tabularx`, `longtable`, `float`, `xcolor`, `listings`, `csquotes`,
`biblatex` con `biblatex-ieee`, y `hyperref`. Además se necesita el programa `biber`.
MiKTeX instala automáticamente los paquetes que falten; en TeX Live vienen incluidos en el
esquema completo (`scheme-full`).
