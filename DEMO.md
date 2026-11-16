# Guia de la demostracion (aprox. 5 minutos)

Repositorio: `aaron-parcial3`. Todo se hace con valores **falsos**: nunca uses una credencial real.

## 0. Preparacion (antes de exponer)

```bash
git clone https://github.com/aarontrjillo15-bot/aaron-parcial3
cd aaron-parcial3
git fetch --all
python -c "import secrets,string; print('sk_live_'+''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(24)))"
```

Copia el token falso que imprime (formato Stripe: GitHub lo reconoce, pero no funciona en ningun servicio).

## 1. Las versiones del programa

| Rama | Comando | Que decir |
|------|---------|-----------|
| `v1.0-insegura` | `git switch v1.0-insegura` | Usa `eval()`: cualquier texto se ejecuta como codigo (CWE-95). |
| `v1.1-segura` | `git switch v1.1-segura` | Evaluador `ast` con lista blanca de operadores y limites. |
| `v1.2-devsecops` | `git switch v1.2-devsecops` | Pruebas, CI, CodeQL, Dependabot, CODEOWNERS y SECURITY.md. |

Prueba visual de la diferencia (en v1.0 se ejecuta el comando; en v1.1 se rechaza):

```bash
python main.py
> __import__("os").system("echo EJECUTADO")
```

Para ver el historial como cadena de hashes: `git log --oneline --graph --all`.

## 2. Branch Protection: `main` no admite push directo

```bash
git switch main
git commit --allow-empty -m "intento directo a main"
git push origin main
```

Resultado esperado: el push es rechazado con `GH006: Protected branch update failed`
(hace falta que la regla de `main` este activa en Settings > Branches).

## 3. Demo principal: Push Protection bloquea un secreto

```bash
git switch demo/commit-en-vivo
```

1. Abre `calculadora/config.py` y reemplaza `REEMPLAZAR_CON_TOKEN_FALSO` por el token falso del paso 0.
2. Guarda el commit y haz push:

```bash
git add calculadora/config.py
git commit -m "feat: agregar configuracion con API key"
git push origin demo/commit-en-vivo
```

Resultado esperado: el push es rechazado por GitHub (`GH013: Repository rule violations`,
`Push cannot contain secrets`) y senala el tipo de secreto (Stripe API Key), el commit y
`calculadora/config.py:<linea>`. Nada llega al repositorio remoto.

Que explicar:
- **Secret Scanning** es detectivo (alerta sobre lo ya expuesto); **Push Protection** es preventivo (bloquea antes de entrar).
- Solo bloquea patrones de proveedores soportados, no contrasenas genericas.
- Quien lo omite debe dar un motivo, queda una alerta y se notifica a los administradores.

## 4. Limpieza correcta y Pull Request

```bash
git reset --hard HEAD~1          # descarta el commit con el secreto (en un caso real, ademas rota la clave)
```

Reemplaza el contenido de `calculadora/config.py` por la version segura (lee de entorno):

```python
import os

API_KEY = os.environ.get("API_KEY", "")
```

```bash
git add calculadora/config.py
git commit -m "feat: leer API key desde variable de entorno"
git push origin demo/commit-en-vivo
```

Abre el Pull Request hacia `main` (usa la plantilla), espera el check `test` y CodeQL, y fusiona.

## 5. CodeQL (SAST) en un Pull Request

La rama `demo/codeql-eval` reintroduce `eval()`. Abre un Pull Request de esa rama hacia `main`:
- CodeQL publica la alerta de **inyeccion de codigo** (CWE-95) en el propio PR.
- El check `test` queda en rojo porque las pruebas de seguridad fallan.
- Ver: pestana Security > Code scanning.

## 6. Dependabot (CVE)

`requirements.txt` fija `requests==2.19.1` a proposito. En Security > Dependabot aparecen las alertas con su CVE
y severidad, y Dependabot abre un Pull Request con la version corregida.

## 7. Trazabilidad con Issues

Crea un Issue (por ejemplo, "Alerta: secreto expuesto en config.py"), trabaja en una rama `fix/<n>` y en el
Pull Request escribe `Fixes #<n>`. Al fusionar, el Issue se cierra solo y queda el rastro completo.
