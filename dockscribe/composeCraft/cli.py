import threading

import typer

from .utils import get_app_data_path
from ..container.utils import exitIfBadToken

app = typer.Typer()

@app.command()
def login(token:str=None) -> None:
    """
    Login to composecraft.com
    """
    if token :
        print("Using token")
        return
    try:
        from .server import run_server
        server_thread = threading.Thread(target=run_server, args=(5555,), daemon=True)
        server_thread.start()
        server_thread.join()
    except Exception :
        print("Your system does not support login through browser.\nYou can use the cmd : $ dockscribe login --token=YOUR_TOKEN")

@app.command()
def check_login(show_config:bool=False)->None:
    """
    Check login status to composecraft.com
    """
    if show_config :
        print(f"the config file is locateed under {get_app_data_path()+'/config.json'}")
    exitIfBadToken()
    print("The config is valid and you are logged in")

if __name__ == "__main__":
    app()