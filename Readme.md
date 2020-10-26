#Basic Auth y OAuth2 Google
Instalar las librerias de dependencia.
```sh
$ pip install requirements.txt
```
Adicionar las variables de entorno al sistema descritas en el archivo [configuration](./app/configuration.py)

Para ejecutar la aplicación levantar desde uvicorn
```sh
$ uvicorn app.main:app --reload
```
