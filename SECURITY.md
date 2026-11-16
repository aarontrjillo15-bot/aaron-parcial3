# Politica de seguridad

Este repositorio es un proyecto academico. Para reportar una vulnerabilidad, abre un
*Security Advisory* privado desde la pestana **Security** del repositorio.

## Controles activos
- Ramas protegidas (`main`): Pull Request obligatorio y pruebas en verde.
- CodeQL (SAST) en cada push y Pull Request.
- Dependabot para alertas y actualizaciones de dependencias.
- Secret Scanning y Push Protection para bloquear credenciales.
- Las credenciales nunca se guardan en el codigo: se leen de variables de entorno (ver `.env.example`).
