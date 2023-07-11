import datetime
import os
import pandas as pd
from celery import Celery
from celery.schedules import crontab
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from constants import dataset_table
from urllib.parse import urlparse

# We define our celery broker. REDIS_URL is generated automatically on Dash Enterprise
# when your app is linked to a Redis Database
# If the app is running on Workspaces, we connect to the same Redis instance as the deployed app but a different Redis
# database
if os.environ.get("DASH_ENTERPRISE_ENV") == "WORKSPACE":
    parsed_url = urlparse(os.environ.get("REDIS_URL"))
    if parsed_url.path == "" or parsed_url.path == "/":
        i = 0
    else:
        try:
            i = int(parsed_url.path[1:])
        except:
            raise Exception("Redis database should be a number")
    parsed_url = parsed_url._replace(path="/{}".format((i + 1) % 16))

    updated_url = parsed_url.geturl()
    REDIS_URL = "redis://%s" % (updated_url.split("://")[1])
else:
    REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

celery_app = Celery(
    "Celery App", broker=REDIS_URL
)

# Create a SQLAlchemy connection string from the environment variable `DATABASE_URL`
# automatically created in your dash app when it is linked to a postgres container
# on Dash Enterprise. If you're running locally and `DATABASE_URL` is not defined,
# then this will fall back to a connection string for a local postgres instance
#  with username='postgres' and password='password'
connection_string = "postgresql+pg8000" + os.environ.get(
    "DATABASE_URL", "postgresql://postgres:password@127.0.0.1:5432"
).lstrip("postgresql")


# Create a SQLAlchemy engine object. This object initiates a connection pool
# so we create it once here and import into app.py.
# `poolclass=NullPool` prevents the Engine from using any connection more than once. You'll find more info here:
# https://docs.sqlalchemy.org/en/14/core/pooling.html#using-connection-pools-with-multiprocessing-or-os-fork
postgres_engine = create_engine(connection_string, poolclass=NullPool)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # This command invokes a celery task at an interval of every 5 seconds. You can change this.
    sender.add_periodic_task(5, update_data.s(), name="Update data")

    # Replace and overwrite this table every Monday at 7:30 am using df.to_sql's `if_exists` argument
    # so that this randomly generated data doesn't grow out of control.
    sender.add_periodic_task(
        crontab(minute=30, hour="7", day_of_week=1),
        update_data.s(if_exists="replace"),
        name="Reset data",
    )


@celery_app.task
def update_data(if_exists="append"):

    # create a list of strings representing the last five seconds
    dates = []
    for i in range(5):
        new_date = datetime.datetime.now() + datetime.timedelta(seconds=-i)
        dates.append(new_date.strftime("%Y-%m-%d %H:%M:%S"))
    dates.reverse()

    # Set a new random seed. Otherwise the seed from the pre-forked process will be used
    # by the celery worker (so we'd always get the same 5 random numbers).
    np.random.seed()
    random_values = np.random.randn(5)

    # In this example, we're just supplying random data to demonstrate that the data has changed.
    # But in practice, you can use this function to query real time data from APIs, databases, or
    # long running models.
    df = pd.DataFrame({"time": dates, "value": random_values})

    # In the following command, we are saving the updated new data to the dataset_table using pandas
    # and the SQLAlchemy engine we created above. When if_exists='append' we add the rows to our table
    # and when if_exists='replace', a new table overwrites the old one.
    df.to_sql(dataset_table, postgres_engine, if_exists=if_exists, index=False)

    return
