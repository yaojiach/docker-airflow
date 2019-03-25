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

- Change `requirements.txt` to `Pipfile`

- `CeleryExecutor`


## References

- https://github.com/puckel/docker-airflow
