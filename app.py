import os
from flask import Flask
import sqlalchemy
from sqlalchemy import text

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of Postgres."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_host = os.environ.get('INSTANCE_HOST', 'localhost')
    db_user = os.environ.get("DB_USER", 'test')
    db_pass = os.environ.get("DB_PASS", 'test')
    db_name = os.environ.get("DB_NAME", 'test')
    db_port = os.environ.get("DB_PORT", 5432)

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
        echo_pool=True,
        echo=True
    )
    return pool


app = Flask(__name__)
pool = connect_tcp_socket()

@app.route('/')
def hello():
    conn = pool.connect()
    conn.execute(text("select * from pg_stat_activity where datname = 'test'"))
    return 'Hello, World!'
