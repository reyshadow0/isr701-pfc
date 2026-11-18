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
| `src/` | Servicios del esqueleto |
| `docs/main.tex` | Archivo principal del documento |
| `docs/secciones/` | Una sección del documento por archivo |
| `docs/referencias.bib` | Referencias (BibLaTeX, estilo IEEE) |
| `docs/figuras/` | Figuras del documento |
| `docs/diagramas/` | Diagramas C4 editables y sus exportaciones |
| `docs/adr/` | Registros de decisiones de arquitectura (ADR) |
| `docs/main.pdf` | Documento compilado |
| `evidencias/` | Levantamiento de información, fotografías de las sesiones y capturas del esqueleto |
| `BITACORA.md` | Bitácora de las sesiones de trabajo del equipo |

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
