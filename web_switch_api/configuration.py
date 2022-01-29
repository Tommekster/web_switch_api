import configparser
from typing import Dict, List
from pydantic import BaseModel
from datetime import timedelta
import re


class ServerConfig(BaseModel):
    host: str
    port: int


class JwtConfig(BaseModel):
    secret_key: str
    algorithm: str


class AuthenticationConfig(BaseModel):
    expiration_time: timedelta


class ReactAppConfig(BaseModel):
    path: str


class SwitchesConfig(BaseModel):
    api_url: str
    switch_names: Dict[int, str]


class CaptivePortalConfig(BaseModel):
    image_path: str


class ConfigurationProvider:
    def __init__(self, conf_file: str = "server.conf"):
        self.config = configparser.ConfigParser()
        self.config.read(conf_file)

    def get_server_config(self) -> ServerConfig:
        section = self.config["Server"]
        return ServerConfig(host=section["host"], port=section.getint("port"))

    def get_jwt_config(self) -> JwtConfig:
        section = self.config["JWT"]
        return JwtConfig(**dict(section))

    def get_authentication_config(self) -> AuthenticationConfig:
        section = self.config["Authentication"]
        units = [
            ("w", "weeks"),
            ("d", "days"),
            ("h", "hours"),
            ("m", "minutes"),
            ("s", "seconds"),
            ("ms", "milliseconds"),
            ("us", "microseconds"),
        ]
        pattern = "".join(
            f"((?P<{param}>\\d+){unit})?"
            for unit, param in units
        )
        match = re.match(pattern, section["expiration_time"])
        if not match:
            raise ValueError("Bad format of expiration_time in Authentication")
        values = {param: int(match.group(param) or 0) for _, param in units}
        expiration_time = timedelta(**values)
        return AuthenticationConfig(expiration_time=expiration_time)

    def get_react_app_config(self) -> ReactAppConfig:
        section = self.config["ReactApp"]
        return ReactAppConfig(**dict(section))

    def get_switches_config(self) -> SwitchesConfig:
        section = self.config["Switches"]
        switche_names = dict(section)
        del switche_names["api_url"]
        return SwitchesConfig(api_url=section["api_url"], switch_names=switche_names)

    def get_captive_portal_config(self) -> CaptivePortalConfig:
        section = self.config["CaptivePortal"]
        return CaptivePortalConfig(**dict(section))


class User(BaseModel):
    id: int
    username: str
    email: str
    roles: List[str]
    password: str


class UsersRepository:
    def __init__(self, conf_file: str = "users.conf"):
        self.conf_file = conf_file
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file)

    def get_users(self) -> List[User]:
        pattern = re.compile(r"User_(?P<id>\d+)")
        users = [
            User(id=int(m.group("id")), **self.config[m.string])
            for m in (pattern.match(s) for s in self.config.keys())
            if m
        ]
        return users

    def save_user(self, user: User) -> None:
        data = user.dict()
        del data["id"]
        self.config[f"User_{user.id}"] = data
        with open(self.conf_file, "w") as f:
            self.config.write(f)


provider = ConfigurationProvider()
users = UsersRepository()
