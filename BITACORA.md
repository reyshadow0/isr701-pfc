# Bitácora del equipo BCCP

## Sesión del miércoles 18 de noviembre de 2026

### Quiénes participamos y cómo trabajamos

Estuvimos los cuatro: Dariem Benites, Jilmar Cedeño, Mario Castro y Steven Pozo. Como cada uno trabajó desde su casa, la sesión fue por WhatsApp y GitHub.

### Qué decidimos

- Elegimos como tema el **Sistema de gestión de documentos de pre-sustentaciones de trabajos de titulación de la UTEQ**.
- Repartimos los roles: Dariem será el arquitecto, Mario el líder de desarrollo, Jilmar el responsable de calidad y Steven el responsable de documentación.
- Trabajaremos en el repositorio público `reyshadow0/isr701-pfc`. Cada uno tendrá su propia rama y todo cambio entrará a `main` por pull request. Dejamos `main` protegida.
- Armamos el tablero en GitHub Projects y asignamos a cada responsable sus issues de E1 y E2.
- E1 vence el domingo 22 de noviembre de 2026 a las 23:59, según el SGA. No vamos a esperar las actividades formativas FORM-TL-02 y FORM-IC-01.
- Quedamos en entrevistar a la Ing. Nancy Rodríguez el jueves 19 de noviembre de 2026 a las 15:00. Llevaremos impresos el acta y el consentimiento.
- Cada uno sacó un riesgo a partir de su caso de FORM-AC-01, y Jilmar juntó los cinco en la sección 11.
- Dividimos el resumen de los ADR en dos archivos: uno lo hace Dariem y el otro Mario.

### Problemas que surgieron y cómo los resolvimos

- Dos de nosotros íbamos a editar el mismo archivo de los ADR, así que separamos el contenido en dos archivos para evitar conflictos.
- Cabía la posibilidad de subir algo directamente a `main` por error, por lo que configuramos una regla para que todo pase por pull request.
- Las claves de las citas todavía no estaban en `main`. Jilmar dejará los enlaces temporales hasta que se fusione el pull request de `referencias.bib`.
- Al revisar `referencias.bib`, vimos que algunos títulos y un autor no coincidían con lo publicado en las páginas originales. Los corregimos antes del merge.
- El apellido de Dariem estaba mal escrito en R03. Ya lo corregimos antes del merge.

### Pendiente

- Tomarnos la foto de la sesión mañana, jueves 19 de noviembre de 2026, cuando nos reunamos.
