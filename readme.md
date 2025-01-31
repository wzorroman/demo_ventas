# Proyecto de procesos
Es un proyecto basado en Django y SqLite

 Versiones:
 - python version: 3.10
 - Django version: 4.2
 

# Instalando el proyecto

  ## Construir la imagen de Docker
  `docker-compose build`

  ## Levantar el contenedor
  `docker-compose up`


## levantar el Docker con las variables ".env" personalizadas:
  `docker compose --env-file app/.env up --build`
    - **Nota**: El archivo *.env* debe estar a la misma altura de *manage.py*, hacer una copia: *.env_sample*


## Cargar la preData:
   `docker exec -ti ventas_django-web python3 manage.py loaddata fixtures/001_user_base.json`

## Correr test:   
   `docker exec -ti ventas_django-web python3 manage.py test apps.base.tests.tests`

## Visit webSite: 
  `http://0.0.0.0:8001/` or `http://localhost:8001/admin`

## Usuarios default:
  | Rol           | Usuario     | pass     |
  |---------------|-------------|----------|
  | Administrador | admin       | admin    |


# ---------------
# Cargar archivo CSV

  - Se tiene los siguientes campos para el archivo CSV


  |descripcion | cantidad | precio | fecha               |
  |------------|----------|--------|--------------------|
  |pelotas     |    6     | 1.20   | 2025-01-29 13:31:13|

  - descripcion : str
  - cantidad: int
  - precio: float
  - fecha : YYYY-MM-DD HH:MM:SS

# ---------------
# Adicionales


 - Para iniciar el docker en local luego de haber creado las images y instancias:
   ```sh
    $ docker start ventas_django-web_1
   ```
      
 - Para destruir el docker en local:
   ```sh
    $ docker stop ventas_django-web
    $ docker image rm ventas_django-web:latest
   ```
   