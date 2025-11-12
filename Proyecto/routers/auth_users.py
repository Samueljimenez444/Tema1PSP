from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pwdlib import PasswordHash
import jwt

import datetime
from jwt.exceptions import InvalidTokenError
import routers
from Proyecto.routers.auth_users import ALGORITHM

# Configuración OAuth2
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Configuración JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "14d0e194f16cad62eb2f966fae845984d720db01d7c72524b9f8fd82f07b45a0"

# Instanciamos el hash
password_hash = PasswordHash.recommended()

# Router
router = APIRouter(
    prefix="/auth_users",
    tags=["auth_users"]
)

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "elenarg": {
        "username": "elenarg",
        "fullname": "Elena Rivero",
        "email": "elana@iesnervion.es",
        "disabled": False,
        "password": "123456"
    },
    "paquito": {
        "username": "Samueljm",
        "fullname": "Samuel Jimenez",
        "email": "samuel.jimenez@iesnervion.es",
        "disabled": False,
        "password": "123456"
    }
}


@router.post("/register", status_code=201)
def register(user: UserDB):
    if user.username not in users_db:
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password
        users_db[user.username] = user.model_dump()
        return user
    else:
        raise HTTPException(status_code=409, detail="User already exists")
    
@router.post("/login")
async def login (form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if user_db:
        user = UserDB(**user_db)
        # Si el usuario existe en la base de datos
        # Comprobamos las contraseñas
        if password_hash.verify(user.password, user["password"]):
            expire = datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = {"sub" : user.username, "exp" : expire}
            # Generamos token
            token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token":token, "token_type":"bearer"}
    raise HTTPException(status_code=401, detail="Usuario o contraseña icorrectos")


async def authentication(token : str= Depends(oauth2)):

    try:
        username= jwt.decode(token,SECRET_KEY,algorithm=ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Creedenciales invalidas",headers=({"WWW-Authenticate" : "Bearer"} ))
        
    except jwt.PyJWTError:

        raise HTTPException(status_code=401,detail="Creedenciales invalidas",headers=({"WWW-Authenticate" : "Bearer"} ))
    
    user = User(**users_db[username])
    