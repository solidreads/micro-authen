# Microservicio para el dominio de usuario

Crear migraciones con alembic

```shell
alembic revision --autogenerate -m "modificar usaurio"
```
Correr las migraciones
```shell
alembic upgrade head
```