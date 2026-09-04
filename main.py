import os
import asyncio
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from models import Package
from dijkstra_service import next_hop, full_route, load_graph_from_registry_or_file
from node_registry import register_self, get_online_nodes
from forwarder import forward_package
from package_store import load_packages, save_packages, STATE_FILE

CITY_NAME = os.environ["CITY_NAME"]
REGISTRY_URL = os.environ["REGISTRY_URL"]
NODE_URL = os.environ["NODE_URL"]

graph: dict[str, list[tuple[str, int]]] = {}
received_packages: list[Package] = load_packages(STATE_FILE)


async def heartbeat_loop():
    while True:
        await asyncio.sleep(3600)
        await register_self(REGISTRY_URL, CITY_NAME, NODE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global graph
    graph = await load_graph_from_registry_or_file(REGISTRY_URL, "cities.csv")

    await register_self(REGISTRY_URL, CITY_NAME, NODE_URL)
    task = asyncio.create_task(heartbeat_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)
started_at = datetime.now(timezone.utc)


app = FastAPI(lifespan=lifespan)
started_at = datetime.now(timezone.utc)


@app.get("/status")
def get_status():
    return {
        "stad": CITY_NAME,
        "url": NODE_URL,
        "mottagna": len(received_packages),
        "uppeSedanUtc": started_at,
    }


@app.get("/paket")
def list_packages():
    return {
        "stad": CITY_NAME,
        "mottagna": received_packages,
    }


@app.post("/paket")
async def receive_package(package: Package):
    package.history.append(CITY_NAME)

    if package.destination.casefold() == CITY_NAME.casefold():
        received_packages.append(package)
        save_packages(STATE_FILE, received_packages)
        return {
            "status": "levererat",
            "stad": CITY_NAME,
            "paket": package,
        }

    else:
        online_nodes = await get_online_nodes(REGISTRY_URL)
        next_city = next_hop(graph, CITY_NAME, package.destination, package.history, set(online_nodes))

        if next_city is None:
            return JSONResponse(status_code=422, content={
                "fel": f"ingen rutt till {package.destination} hittades",
                "onlineNoder": list(online_nodes.keys()),
                "historik": package.history,
            })

        success = await forward_package(online_nodes[next_city], package)

        if not success:
            return JSONResponse(status_code=502, content={"fel": f"kunde inte nå {next_city}"})

        return {
            "status": "vidarebefordrat",
            "nästaHopp": next_city,
            "paket": package,
        }


@app.get("/route")
async def get_route(from_city: str = Query(alias="from"), to_city: str = Query(alias="to")):
    online_nodes = await get_online_nodes(REGISTRY_URL)
    route = full_route(graph, from_city, to_city, set(online_nodes))

    if len(route) < 2:
        return JSONResponse(status_code=404, content={
            "fel": f"Ingen rutt från {from_city} till {to_city} med nuvarande noder online",
            "onlineNoder": list(online_nodes.keys()),
        })

    return {
        "från": from_city,
        "till": to_city,
        "rutt": route,
        "antalStopp": len(route) - 2,
    }


@app.post("/forceheartbeat")
async def force_heartbeat():
    await register_self(REGISTRY_URL, CITY_NAME, NODE_URL)
    return {"status": "heartbeat"}