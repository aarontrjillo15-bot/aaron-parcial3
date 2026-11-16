# aaron-parcial3

Calculadora en Python (version de consola y version con ventana y botones) usada como caso practico de **desarrollo seguro con Git y GitHub**
(parcial 3). El programa es simple a proposito: lo importante son los controles que lo rodean.

## Uso

```bash
python calculadora_visual.py                # calculadora con ventana y botones (tkinter)
python main.py                              # calculadora de consola
python -m unittest discover -s tests -v     # pruebas
```

La ventana acepta el raton y el teclado (digitos, `+ - * / ^ %`, parentesis, Enter, Retroceso,
Esc para limpiar), guarda un historial y muestra los errores en pantalla. Usa el mismo evaluador
seguro (`calculadora/core.py`, sin `eval`): los botones solo pueden producir teclas validas.
`tkinter` viene con Python en Windows y macOS; en Linux: `sudo apt install python3-tk`.

## Versiones (una rama por version)

| Rama | Que muestra |
|------|-------------|
| `v1.0-insegura` | Primera version. Usa `eval()` sobre la entrada del usuario (CWE-95). CodeQL la detecta. |
| `v1.1-segura` | Reemplaza `eval()` por un evaluador `ast` con lista blanca de operadores y limites. |
| `v1.2-devsecops` | Agrega pruebas, CI, CodeQL, Dependabot, CODEOWNERS, plantilla de PR y politica de seguridad. |
| `main` | Ultima version estable (v1.3: agrega la calculadora con ventana), protegida: no admite push directo. |
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

Demo en vivo: cambio de prueba.

Demo en vivo: cambio de prueba.
