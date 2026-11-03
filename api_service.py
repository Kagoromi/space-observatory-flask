import requests

NASA_API_URL = "https://images-api.nasa.gov/search"

def search_external_api(query):
    # Task 1 and 2: Request to external NASA API
    params = {
        "q": query,
        "media_type": "image"
    }
    
    # Task 4: Timeout check
    response = requests.get(NASA_API_URL, params=params, timeout=5)
    response.raise_for_status()
    
    data = response.json()
    items = data.get("collection", {}).get("items", [])
    
    results = []
    for item in items[:12]:
        data_list = item.get("data", [])
        if not data_list:
            continue
        
        info = data_list[0]
        
        # Task 5: Parse 4 fields
        results.append({
            "external_id": info.get("nasa_id", ""),
            "title": info.get("title", "Untitled"),
            "center": info.get("center", "NASA"),
            "date_created": info.get("date_created", "Unknown")[:10]
        })
        
    return results