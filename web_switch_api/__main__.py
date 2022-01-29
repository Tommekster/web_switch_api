if __name__ == "__main__":
    import uvicorn
    from .configuration import provider
    from .main import app

    config = provider.get_server_config()

    uvicorn.run(app, host=config.host, port=config.port)
