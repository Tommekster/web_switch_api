if __name__ == "__main__":
    import uvicorn
    from .main import app
    uvicorn.run(app, host="0.0.0.0", port=5000)
