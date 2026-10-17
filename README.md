# Campus API Segura 🚀

API REST desarrollada con **FastAPI** para la gestión y autenticación de usuarios mediante **OAuth2** y tokens **JWT**, implementando buenas prácticas de seguridad y hashing de contraseñas con **Argon2**.

---

## 🛠️ Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno y de alto rendimiento.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para ejecutar la aplicación.
- **[PyJWT](https://pyjwt.readthedocs.io/)**: Generación y verificación de JSON Web Tokens (JWT).
- **[pwdlib (Argon2)](https://frankie567.github.io/pwdlib/)**: Hashing seguro de contraseñas.
- **[Pydantic](https://docs.pydantic.dev/)**: Validación y serialización de datos.
- **[python-dotenv](https://github.com/theskumar/python-dotenv)**: Gestión de variables de entorno.

---

## 📋 Requisitos Previos

- **Python 3.10+** (recomendado 3.12)
- **pip** instalado

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_CARPETA>
```

### 2. Crear y activar el entorno virtual

- **En Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto a partir de `.env.example`:

```env
JWT_SECRET_KEY=tu_clave_secreta_super_segura
JWT_ALGORITHM=HS256
MINUTOS_EXPIRACION=30
```

> [!TIP]
> Puedes generar una clave segura con: `python -c "import secrets; print(secrets.token_hex(32))"`

### 5. Iniciar el servidor de desarrollo
```bash
fastapi dev main.py
```
*O con Uvicorn directamente:*
```bash
uvicorn main:app --reload
```

El servidor estará escuchando en `http://127.0.0.1:8000`.

---

## 📖 Documentación Interactiva

FastAPI genera documentación interactiva automáticamente. Una vez iniciado el servidor, puedes acceder a:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 Rutas de la API

| Método | Endpoint | Acceso | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/publico` | Público | Mensaje de bienvenida sin requerir autenticación. |
| `POST` | `/usuarios/registro` | Público | Registra un nuevo usuario hasheando la contraseña con Argon2. |
| `POST` | `/token` | Público | Inicia sesión (OAuth2 Password Request Form) y retorna el token JWT. |
| `GET` | `/cursos` | 🔒 Protegido | Retorna el catálogo de cursos para el usuario autenticado. |
| `GET` | `/perfil` | 🔒 Protegido | Retorna la información de perfil del usuario autenticado. |

---

## 🔐 Flujo de Autenticación

1. **Registro:** Envía un `POST` a `/usuarios/registro` con `username` y `password`.
2. **Login:** Envía las credenciales vía `POST` a `/token` para obtener un `access_token`.
3. **Peticiones protegidas:** En las rutas protegidas, incluye la cabecera HTTP:
   ```http
   Authorization: Bearer <TU_ACCESS_TOKEN>
   ```
   *(En Swagger UI puedes usar directamente el botón verde **Authorize** en la parte superior).*

---

## 📁 Estructura del Proyecto

```text
├── .env                # Variables de entorno (ignorado en git)
├── .env.example        # Plantilla de variables de entorno
├── .gitignore          # Reglas de exclusión para Git
├── requirements.txt    # Dependencias del proyecto
├── main.py             # Código fuente de la API y rutas
└── README.md           # Documentación del proyecto
```
