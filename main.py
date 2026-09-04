import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from datetime import datetime, timezone

from models import Package
from dijkstra_service import load_graph, next_hop, full_route
from node_registry import register_self, get_online_nodes
from forwarder import forward_package
from fastapi.responses import JSONResponse


CITY_NAME = os.environ["CITY_NAME"]
REGISTRY_URL = os.environ["REGISTRY_URL"]
NODE_URL = os.environ["NODE_URL"]

graph = load_graph("cities.csv")

recieved_packages: list[Package] = []

async def heartbeat_loop():
    while True:
        await asyncio.sleep(3600)
        await register_self(REGISTRY_URL, CITY_NAME, NODE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await register_self(REGISTRY_URL, CITY_NAME, NODE_URL)
    task = asyncio.create_task(heartbeat_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)

started_at = datetime.now(timezone.cet)

app = FastAPI(lifespan=lifespan)

@app.get("/status")
def get_status():
    return {
        "stad": CITY_NAME,
        "url": NODE_URL,
        "mottagna": len(recieved_packages),
        "uppeSedanCet": started_at,
    }

@app.get("/paket")
def list_packages():
    return{
        "stad": CITY_NAME,
        "mottagna": len(recieved_packages),
    }

@app.post("/paket")
async def receive_package(package: Package):
    package.history.append(CITY_NAME)
    if package.destination.casefold() == CITY_NAME.casefold():
        return {
            "status": "levererat",
            "stad": CITY_NAME,
            "paket": package,
        }
    else:
        online_nodes = await get_online_nodes(REGISTRY_URL)
        next_city = next_hop(graph, CITY_NAME, package.destination, package.history, online_nodes.keys())

        if next_city is None:
            return JSONResponse(status_code=422, content={
                "fel": "ingen rutt till {package.destination} hittades.",
                "onlineNoder": list(online_nodes.keys()),
                "historik": package.history,
                })

        success = await forward_package(online_nodes[next_city], package)

        if not success:
            return JSONResponse(status_code=502, content={"fel": f"kunde inte nå {next_city}"})

        return {
            "status": "Vidarebefordrat",
            "nästaHopp": next_city,
            "paket": package,
        }
    