# Como rodar o projeto

Tem que ter o Python instalado.
Aí roda

```sh
pip install -r requirements.txt
```

pra instalar os pacotes que precisa.

Tem dois comandos agora:

Roda isso no diretório inicial pra rodar o projeto:
```sh
flask --app projeto run --debug
```

Roda isso pra rodar o schema.sql que deleta as tabelas anteriores e coloca as novas que tão lá:
```
flask --app projeto init-db
```
