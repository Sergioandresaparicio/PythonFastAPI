import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Campus API segura")

CLAVE_SECRETA = os.getenv("JWT_SECRET_KEY")
if CLAVE_SECRETA is None:
    raise ValueError("No se encontró la CLAVE_SECRETA en el archivo .env")

ALGORITMO = os.getenv("JWT_ALGORITHM")
if ALGORITMO is None:
    raise ValueError("No se encontró el ALGORITMO en el archivo .env")

MINUTOS_EXPIRACION = 30

usuarios_db = {}

contexto_password = PasswordHash.recommended()

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="token")


class UsuarioRegistro(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=20)


class RespuestaToken(BaseModel):
    access_token: str
    token_type: str


def hashear_password(password: str) -> str:
    """Genera un hash seguro a partir de una contraseña en texto plano utilizando Argon2."""
    return contexto_password.hash(password)


def verificar_password(password: str, hash: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return contexto_password.verify(password, hash)


@app.post("/usuarios/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioRegistro):
    """Registra un nuevo usuario en la base de datos simulada."""
    if usuario.username in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya existe"
        )

    pwd_hash = hashear_password(usuario.password)
    usuarios_db[usuario.username] = {
        "username": usuario.username,
        "password": pwd_hash,
        "password_hash": pwd_hash
    }
    return {
        "mensaje": "Usuario registrado exitosamente",
        "username": usuario.username
    }


def crear_token_acceso(username: str) -> str:
    """Crea un token JWT que incluye los claims obligatorios 'sub' y 'exp'."""
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    payload = {
        "sub": username,
        "username": username,
        "exp": expiracion
    }
    token = jwt.encode(payload, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token


@app.post("/token", response_model=RespuestaToken)
def iniciar_sesion(formulario: OAuth2PasswordRequestForm = Depends()):
    """Autentica al usuario y devuelve el token de acceso JWT."""
    usuario = usuarios_db.get(formulario.username)
    hash_almacenado = usuario.get("password_hash") or usuario.get("password") if usuario else None
    
    if not usuario or not verificar_password(formulario.password, hash_almacenado):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = crear_token_acceso(usuario["username"])
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def obtener_usuario_actual(token: str = Depends(esquema_oauth2)) -> dict:
    """Decodifica y valida el token JWT con claims obligatorios y retorna el usuario actual."""
    try:
        payload = jwt.decode(
            token,
            CLAVE_SECRETA,
            algorithms=[ALGORITMO],
            options={"require": ["sub", "exp"]}
        )
        username = payload.get("sub")

        if not isinstance(username, str) or not username:
            raise ValueError("Token sin usuario valido")
    except (InvalidTokenError, jwt.PyJWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario = usuarios_db.get(username)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return usuario


@app.get("/publico")
def publico():
    """Ruta pública sin autenticación."""
    return {
        "mensaje": "Bienvenido a Campus API"
    }


@app.get("/cursos")
def cursos(usuario_actual: dict = Depends(obtener_usuario_actual)):
    """Catálogo de cursos disponibles."""
    return {
        "usuario": usuario_actual["username"],
        "cursos": ["Python", "Java", "FastAPI"]
    }

@app.get("/perfil")
def perfil(usuario_actual: dict = Depends(obtener_usuario_actual)):
    """Ruta protegida que devuelve la información del usuario autenticado."""
    return {
        "mensaje": "acceso concedido",
        "usuario": usuario_actual["username"],
        "cursos": ["Python", "Java", "FastAPI"]
    }