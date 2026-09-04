import httpx
from models import Package

async def forward_package(node_url: str, package: Package) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{node_url}/paket",
                json=package.model_dump(by_alias=True),
            )
            response.raise_for_status()
            return True
    except httpx.HTTPError as err:
        return False