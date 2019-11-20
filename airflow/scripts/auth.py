# import airflow
# from airflow import models, settings
# from airflow.contrib.auth.backends.password_auth import PasswordUser


# user = PasswordUser(models.User())
# user.username = 'admin'
# user.email = 'admin@mail.box'
# user.password = 'admin'

# session = settings.Session()
# session.add(user)
# session.commit()
# session.close()

# alternative
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'user'
user.email = 'user@email.com'
user.password = 'password'

from sqlalchemy import create_engine
engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")

session = settings.Session(bind=engine)
session.add(user)
session.commit()
session.close()
