from typing import Dict

from pydantic import Field, SecretStr, BaseModel

from sqlalchemy import URL


class DatabaseConfig(BaseModel):
    driver: str = Field(default='postgresql+asyncpg')
    database: str = Field(default='database')
    user: str = Field(default='user')
    password: SecretStr = Field(default='password')
    host: str = Field(default='postgres')
    host_alembic: str = Field(default='postgres')
    port: int = Field(default=5432)

    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)
    pool_size: int = Field(default=5)
    max_overflow: int = Field(default=10)

    naming_convention: Dict[str, str] = Field(
        default= {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    )

    def build_url(
        self,
        host: str
    ) -> str:
        return URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password.get_secret_value(),
            host=host,
            port=self.port,
            database=self.database
        ).render_as_string(
            hide_password=False
        )

__all__ = ['DatabaseConfig']