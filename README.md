# aaron-parcial3

Calculadora de consola en Python usada como caso practico de **desarrollo seguro con Git y GitHub**
(parcial 3). El programa es simple a proposito: lo importante son los controles que lo rodean.

## Uso

```bash
python main.py                              # calculadora interactiva
python -m unittest discover -s tests -v     # pruebas
```

## Versiones (una rama por version)

| Rama | Que muestra |
|------|-------------|
| `v1.0-insegura` | Primera version. Usa `eval()` sobre la entrada del usuario (CWE-95). CodeQL la detecta. |
| `v1.1-segura` | Reemplaza `eval()` por un evaluador `ast` con lista blanca de operadores y limites. |
| `v1.2-devsecops` | Agrega pruebas, CI, CodeQL, Dependabot, CODEOWNERS, plantilla de PR y politica de seguridad. |
| `main` | Ultima version estable, protegida: no admite push directo. |
| `demo/commit-en-vivo` | Lista para la demostracion: aqui se sube el commit con un secreto falso. |

## Controles de seguridad

| Control | Donde esta |
|---------|-----------|
| Branch Protection en `main` | Settings > Branches (PR obligatorio, pruebas en verde, sin force push) |
| SAST con CodeQL | `.github/workflows/codeql.yml` |
| Dependabot (CVE) | `.github/dependabot.yml` + `requirements.txt` con una version antigua a proposito |
| Secret Scanning + Push Protection | Settings > Code security |
| Revision obligatoria | `.github/CODEOWNERS` y `.github/pull_request_template.md` |
| Politica de reporte | `SECURITY.md` |

La guia paso a paso de la demostracion esta en [`DEMO.md`](DEMO.md).
