from fastapi.staticfiles import StaticFiles
from . import configuration

config = configuration.provider.get_react_app_config()


class ReactStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response
