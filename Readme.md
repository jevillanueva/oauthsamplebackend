# Basic Auth y OAuth2 Google
Instalar las librerias de dependencia.
```sh
$ pip install requirements.txt
```
Adicionar las variables de entorno al sistema descritas en el archivo [configuration](./app/configuration.py)

Para ejecutar la aplicación levantar desde uvicorn
```sh
$ uvicorn app.main:app --reload --host 0.0.0.0
```
## Para crear la imagen de Docker y ejecutar
```sh
$ docker build . -t jv/fastapioauth
```
Para ejecutar utilizando un archivo .env.development.local donde este definidas las variables de entorno.
```sh
$ docker run --env-file .\.env.development.local -p 8000:8000 jv/fastapioauth
```
