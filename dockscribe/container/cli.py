import sys
from typing import Annotated

import requests
import typer

from ..config import config
from .analyse import analyse_whole_machine, analyse_compose_file
from .utils import exitIfBadToken, getTokenFromData

app = typer.Typer()

@app.command()
def describe(
        filename: Annotated[str, typer.Option("--filename",'-f',help="Docker compose file to analyse (also works with a compose file url)")] = None,
        include_volumes:Annotated[bool, typer.Option(help="If the volumes are included in the analysis (no effect with --filename )")] = False
)->None:
    """
    Produce a composecraft visualMap of a container system.
    If you specify a file using --filename or -f ,it wll produce a view of the compose file.

    By default, it produces a view of the whole dockers in the system.

    For security reason the env and secrets are never uploaded to analyze.
    """
    exitIfBadToken()
    if filename:
        print(f"describe {filename}")
        compose_file_content_cleaned = analyse_compose_file(filename)
        resp = requests.post(f"{config['url']}/api/compose", json=compose_file_content_cleaned, headers={"Authorization":getTokenFromData() })
        if resp.status_code != 200:
            sys.exit("Failed to describe compose, there is a problem with the API.")
        else :
            print(f"""
Complete analysis 🥳 ! 
            
You can view the compose file at :
\t{config['url']}/dashboard/playground?id={resp.json()['id']}
""")
        return
    print("describe whole container")
    data = analyse_whole_machine(include_volumes)
    resp = requests.post(f"{config['url']}/api/compose/machine", json=data,
                         headers={"Authorization": getTokenFromData()})
    if resp.status_code != 200:
        sys.exit("Failed to describe compose, there is a problem with the API.")
    else:
        print(f"""
        Complete analysis 🥳 ! 

        You can view the compose file at :
        \t{config['url']}/dashboard/playground?id={resp.json()['id']}
        """)
    return