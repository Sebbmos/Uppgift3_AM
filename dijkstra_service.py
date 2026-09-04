
import csv
import heapq

def load_graph(csv_path: str) -> dict[str, list[tuple[str, int]]]:
    graph = {}
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            from_city = row['from'].strip()
            to_city = row['to'].strip()
            km = int(row['km'].strip())

            graph.setdefault(from_city, []).append((to_city, km))
            graph.setdefault(to_city, []).append((from_city, km))

    return graph

def build_lookup(graph: dict[str, list[tuple[str, int]]]) -> dict[str, str]:
    return {city.casefold(): city for city in graph}

# if __name__ == "__main__":
#     graph = load_graph("cities.csv")
#     lookup = build_lookup(graph)
#     print(lookup)

def next_hop(
        graph: dict[str, list[tuple[str, int]]],
        from_city: str,
        to_city: str,
        visited: list[str] | None = None,
        online_nodes: set[str] | None = None
) -> str | None:
    lookup = build_lookup(graph)
    from_city = lookup.get(from_city.casefold(), from_city)
    to_city = lookup.get(to_city.casefold(), to_city)
    skip = {lookup.get(c.casefold(), c) for c in visited}
    online = (
        {lookup.get(c.casefold(), c) for c in online_nodes}
        if online_nodes is not None else None
    )

    distance = {city: float('inf') for city in graph}
    previous = {}
    distance[from_city] = 0

    pq = []
    heapq.heappush(pq, (0, from_city))

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == to_city:
            break

        if current_node not in graph:
            continue

        for neighbor, weight in graph[current_node]:
            is_destination = (neighbor == to_city)
            if neighbor in skip and not is_destination:
                continue
            if online is not None and neighbor not in online and not is_destination:
                continue

            new_distance = current_distance + weight
            if new_distance < distance.get(neighbor, float('inf')):
                distance[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    if to_city not in previous:
        return None

    # Backtrack to find the next hop

    node = to_city

    while node in previous and previous[node] != from_city:
        node = previous[node]

    return node

# if __name__ == "__main__":
#     g = load_graph("cities.csv")
#     result = next_hop(g, "Göteborg", "Umeå", [], online_nodes={"Göteborg", "Malmö", "Jönköping", "Stockholm", "Sundsvall", "Umeå"})
#     print(result)
#     # Expected output: "Jönköping"

def full_route(
        graph: dict[str, list[tuple[str, int]]],
        from_city:  str,
        to_city: str,
        online_nodes: set[str] | None = None,
)       -> list[str]:
        route = [from_city]
        current = from_city

        for _ in range(len(graph)):
            next_city = next_hop(graph, current, to_city, route, online_nodes)
            if next_city is None:
                break
            route.append(next_city)

            if next_city.casefold() == to_city.casefold():
                break
            current = next_city

        return route



g = load_graph("cities.csv")
route = full_route(g, "göteborg", "umeå", online_nodes={"Göteborg", "Malmö", "Jönköping", "Stockholm", "Sundsvall", "Umeå"})
print(route)


