from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String
from config.db import engine, meta_data

users = Table("users", meta_data,
            Column("id", String, primary_key=True),
            Column("email", String, nullable=False),
            Column("password", String, nullable=False),
            Column("first_name", String, nullable=False),
            Column("last_name", String, nullable=False),
            Column("state", String, nullable=False),
            Column("photo", String, nullable=True)
        )

meta_data.create_all(engine)