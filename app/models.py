"""Con esta estructura, un usuario puede tener varios roles, y cada rol puede tener varios permisos. """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Usuario(Base):
    __tablename__ = "usuario"
    id = Column("id", UUID(as_uuid=True), primary_key=True)
    nombre_usuario = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)


class Roles(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True)
    nombre_rol = Column(String(100), nullable=False)
    descripcion = Column(String(100), nullable=True)


class UsuarioRoles(Base):
    __tablename__ = "usuario_roles"
    id = Column(UUID(as_uuid=True), primary_key=True)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))
    id_rol = Column(UUID(as_uuid=True), ForeignKey("roles.id"))


class Permiso(Base):
    __tablename__ = "permiso"
    id = Column(UUID(as_uuid=True), primary_key=True)
    nombre_permiso = Column(String(100), nullable=False)
    descripcion = Column(String(100), nullable=True)


class RolesPermiso(Base):
    __tablename__ = "roles_permiso"
    id = Column(UUID(as_uuid=True), primary_key=True)
    id_rol = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    id_permiso = Column(UUID(as_uuid=True), ForeignKey("permiso.id"))
