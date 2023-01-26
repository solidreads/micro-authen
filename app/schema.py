import uuid

from pydantic import BaseModel, Field, EmailStr


class UsuarioSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    nombre_usuario: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "nombre_usuario": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.com",
                "password": "weakpassword",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {"example": {"email": "abdulazeez@x.com", "password": "weakpassword"}}


class Roles(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    nombre_rol: str = Field(...)
    descripcion: str = Field(...)

    class Config:
        orm_mode = True


class UsuarioRoles(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    id_usuario: str = Field(...)
    id_rol: str = Field(...)

    class Config:
        orm_mode = True


class Permiso(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    nombre_permiso: str = Field(...)
    descripcion: str = Field(...)

    class Config:
        orm_mode = True


class RolesPermiso(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    id_rol: str = Field(...)
    id_permiso: str = Field(...)

    class Config:
        orm_mode = True
