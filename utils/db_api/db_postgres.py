from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_categories(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Category(
        id SERIAL PRIMARY KEY,
        name VARCHAR(200))
        """

        await self.execute(sql, execute=True)

    async def create_table_product(self):
        sql = """
         CREATE TABLE IF NOT EXISTS Product(
         id SERIAL PRIMARY KEY,
         name VARCHAR(200),
         price DECIMAL,
         count INTEGER)
        """

        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, name, username, telegram_id):
        sql = "INSERT INTO app_user (name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, name, username, telegram_id, fetchrow=True)

    async def add_order(self, count, product_id, user_id, price, name):
        sql = "INSERT INTO app_order (count, product_id, user_id, price,name) VALUES($1, $2, $3, $4,$5) returning *"
        return await self.execute(sql, count, product_id, user_id, price, name, fetchrow=True)

    async def add_history(self, user_id, price):
        sql = "INSERT INTO app_history (user_id, price) VALUES($1, $2) returning *"
        return await self.execute(sql, user_id, price, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_categories(self):
        sql = "SELECT * FROM app_category"
        return await self.execute(sql, fetch=True)

    async def select_all_product(self):
        sql = "SELECT * FROM app_product"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_history(self, **kwargs):
        sql = "SELECT * FROM app_history WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_product(self, **kwargs):
        sql = "SELECT * FROM app_product WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_order(self, **kwargs):
        sql = "SELECT * FROM app_order WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_category(self, **kwargs):
        sql = "SELECT * FROM app_category WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_order(self, **kwargs):
        sql = "DELETE FROM app_order WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
