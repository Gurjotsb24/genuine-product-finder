from services.verifier import load_verified_platforms

def search_product(product_name: str, pincode: str):
    """
    Aggregates product listings across verified platforms with location-based ETAs.
    """
    platforms = load_verified_platforms()
    results = []

    # Simple region determination logic based on pincode structure (e.g., tier-1 metro prefixes)
    is_metro = pincode.startswith(("11", "40", "56", "60", "70", "50"))

    for platform in platforms:
        # Determine availability & delivery speed
        if platform["supports_quick_commerce"]:
            if is_metro:
                in_stock = True
                eta = "10 to 15 Minutes"
            else:
                in_stock = False
                eta = "Not available in your pincode"
        elif platform["type"] == "Official Brand Store":
            in_stock = True
            eta = "2 to 3 Days (Direct Brand Guarantee)"
        else:  # E-Commerce & Retail
            in_stock = True
            eta = "1 Day (Same-day/Next-day Delivery)" if is_metro else "2 to 4 Days"

        # Format purchase search URL
        query_encoded = product_name.replace(" ", "+")
        if "amazon" in platform["domain"]:
            buy_url = f"https://www.{platform['domain']}/s?k={query_encoded}"
        else:
            buy_url = f"https://www.{platform['domain']}/search?q={query_encoded}"

        results.append({
            "platform_id": platform["id"],
            "platform_name": platform["name"],
            "platform_type": platform["type"],
            "trust_score": platform["trust_score"],
            "is_verified": True,
            "in_stock": in_stock,
            "estimated_delivery": eta,
            "pincode": pincode,
            "buy_url": buy_url
        })

    return {
        "product_query": product_name,
        "pincode": pincode,
        "total_verified_options": len([r for r in results if r["in_stock"]]),
        "results": results
    }