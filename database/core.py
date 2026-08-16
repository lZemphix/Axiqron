from asyncpg import Connection, connect

from common.configs.settings import settings
from common.utils.enums import StatusCodesEnum
from common.utils.types import Result


class Postgres:
    def __init__(self, user: str, password: str):
        self.host = "0.0.0.0"
        self.port = 5432
        self.user = user
        self.password = password

    async def _get_connection(self) -> Connection:
        return connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
        )

    async def __fabric(self, method: str, query: str, *args):
        conn = await self._get_connection()
        try:
            db_method = getattr(conn, method)
            return await db_method(query, args)
        finally:
            await conn.close()

    async def fetchone(self, query: str, *args) -> Result:
        try:
            res = await self.__fabric("fetchrow", query, args)
            return Result(status=StatusCodesEnum.OK, result=dict(res))
        except NameError as e:
            return Result(
                status=StatusCodesEnum.ERROR,
                message=e,
            )

    async def fetchmany(self, query: str, *args) -> Result:
        try:
            res = await self.__fabric("fetch", query, args)
            return Result(result=list(map(dict, res)))
        except NameError as e:
            return Result(status=StatusCodesEnum.ERROR, message=e)

    async def execute(self, query: str, *args) -> Result:
        try:
            await self.__fabric("execute", query, args)
            return Result()
        except NameError as e:
            return Result(
                status=StatusCodesEnum.ERROR,
                message=e,
            )


postgers = Postgres(user=settings.DB_USER, password=settings.DB_PASSWORD)
