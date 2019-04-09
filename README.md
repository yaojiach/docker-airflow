# Docker Airflow Boilerplate

Uses NGINX in case some companies have policies that do not allow random ports to be open.

- Usage

```sh
docker-compose up --build -d
```

- Generate fernet key

```sh
docker run webserver python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)"
```

- Check airflow webserver logs

```sh
docker logs --tail 50 --follow --timestamps webserver
```


## Todo

- `CeleryExecutor`


## Gotchas

- May need to do this in interactive session to create user if using psql

```python
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
from sqlalchemy import create_engine

user = PasswordUser(models.User())
user.username = 'user'
user.email = 'user@email.com'
user.password = 'password'

engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")
session = settings.Session(bind=engine)
session.add(user)
session.commit()
session.close()
exit()
```


## References

- https://github.com/puckel/docker-airflow
