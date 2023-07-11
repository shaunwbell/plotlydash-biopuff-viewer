### Refresh Data Periodically via the built-in Postgres Database

This application demonstrates how to refresh backend data periodically on a schedule using Celery and save it to a Postgres database on Dash Enterprise.

- To run this application locally, you must run a redis server locally for the celery broker and a local postgres database. Note that you should run the celery process using celery -A tasks worker --loglevel=INFO --concurrency=2 --beat before trying to run app.py for the first time since this app requires a postgres table named dataset_table and this table is created by the celery scheduler.
- To deploy this application, you must create and link a Redis and Postgres database via the App Manager UI.

### Running locally

1. Follow the quickstart Redis installation instructions [here](https://redis.io/topics/quickstart).
2. Run `make install` to instantiate Redis.
3. Run `redis-server` to start Redis.
4. Install postgresql, follow instructions [here](https://www.postgresql.org/download/). If you're on Mac,
   you can use Homebrew.
   ```
   $ brew install postgresql
   ```
5. Initialize your postgres database:
   ```
   initdb /usr/local/var/postgres
   ```
6. Start your postgres database. On Mac:
   ```
   brew services start postgresql
   ```
7. Set temporary environment variable DATABASE_URL:
   ```
   $ export DATABASE_URL="postgres://127.0.0.1:5432"
   ```
8. Run `celery -A tasks worker --loglevel=INFO --concurrency=2 --beat`
9. Run the app with `python app.py` in a separate terminal.

### Running inside a Workspace

[Dash Enterprise Workspaces]({base_url}/Docs/workspaces) is a browser-based development environment for developing Dash apps an environment that closely matches the environment of deployed applications.

In Workspaces, the Redis and Postgres instances are shared between the Workspace and the deployed application. In this sample application, the Redis URL is modified to write to a different Redis _database_ (but the same instance) in `tasks.py` and the Postgres code is modified to write to a different Postgres _table_ (but the same instance) in `constants.py`. If you would like to read from or write to the same table as your deployed application, then you can comment out these lines in `constants.py`.

In two separate terminals, run the following commands:
1. Run `celery -A tasks worker --loglevel=INFO --concurrency=2 --beat`
2. Run the app with `python app.py` in a separate terminal.
