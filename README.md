



# instructions for usage



Migrate the db:

```sh
FLASK_APP = app flask db init
FLASK_APP = app flask db migrate
FLASK_APP = app flask db upgrade
```



```sh
# Unix:
FLASK_APP = app flask run

# Windows:
export or set  FLASK_APP = app   
flask run
