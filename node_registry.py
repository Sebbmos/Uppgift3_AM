import httpx

async def register_self(registry_url: str, city: str, node_url: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{registry_url}/nodes",
            json={"city": city, "url": node_url},
        )
        response.raise_for_status()

async def get_online_nodes(registry_url: str) -> dict[str, str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{registry_url}/nodes")
        response.raise_for_status()

    nodes = response.json()
    return {node["city"]: node["url"] for node in nodes}
