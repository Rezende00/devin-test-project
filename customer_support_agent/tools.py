from typing import Optional

MOCK_ORDERS = {
    "ORD-001": {
        "order_id": "ORD-001",
        "customer_name": "Alice Johnson",
        "product": "Wireless Headphones",
        "status": "delivered",
        "total": 79.99,
        "delivery_date": "2026-02-05",
    },
    "ORD-002": {
        "order_id": "ORD-002",
        "customer_name": "Bob Smith",
        "product": "USB-C Hub",
        "status": "shipped",
        "total": 45.00,
        "tracking_number": "TRK-98765",
    },
    "ORD-003": {
        "order_id": "ORD-003",
        "customer_name": "Carol Davis",
        "product": "Mechanical Keyboard",
        "status": "processing",
        "total": 129.99,
    },
    "ORD-004": {
        "order_id": "ORD-004",
        "customer_name": "David Lee",
        "product": "Monitor Stand",
        "status": "cancelled",
        "total": 34.50,
    },
}

MOCK_KNOWLEDGE_BASE = [
    {
        "id": "KB-001",
        "title": "Return Policy",
        "content": "Items can be returned within 30 days of delivery for a full refund. Items must be in original packaging.",
        "category": "policy",
    },
    {
        "id": "KB-002",
        "title": "Shipping Information",
        "content": "Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days. Free shipping on orders over $50.",
        "category": "shipping",
    },
    {
        "id": "KB-003",
        "title": "Wireless Headphones - Product Info",
        "content": "Bluetooth 5.3, 40-hour battery life, Active Noise Cancellation, USB-C charging. Compatible with all devices.",
        "category": "product",
    },
    {
        "id": "KB-004",
        "title": "Warranty Information",
        "content": "All electronics come with a 1-year manufacturer warranty. Extended warranty available for purchase.",
        "category": "policy",
    },
]


def get_order_status(order_id: str) -> dict:
    """Retrieves the current status and details of a customer order.

    Args:
        order_id: The unique order identifier (e.g., 'ORD-001').

    Returns:
        A dictionary containing order details or an error message.
    """
    # BUG: Returns a nested "data" wrapper that downstream consumers don't expect.
    # The agent and tests expect a flat dict with order fields directly.
    # This causes issues when the agent tries to access response["status"] directly.
    order = MOCK_ORDERS.get(order_id)
    if order:
        return {"data": {"order": order}, "metadata": {"source": "legacy_api"}}
    return {"data": None, "error": f"Order {order_id} not found"}


def refund_order(order_id: str, reason: Optional[str] = None) -> dict:
    """Processes a refund request for a given order.

    Args:
        order_id: The unique order identifier to refund.
        reason: Optional reason for the refund.

    Returns:
        A dictionary with the refund result.
    """
    # BUG: No validation or exception handling for invalid/missing order IDs.
    # If order_id is None, empty, or not in the database, this will either
    # return a confusing success message or crash unexpectedly.
    order = MOCK_ORDERS[order_id]  # KeyError if order_id not found

    if order["status"] == "cancelled":
        return {
            "status": "error",
            "message": f"Order {order_id} is already cancelled and cannot be refunded.",
        }

    refund_amount = order["total"]
    return {
        "status": "success",
        "order_id": order_id,
        "refund_amount": refund_amount,
        "message": f"Refund of ${refund_amount:.2f} processed for order {order_id}.",
    }


def search_knowledge_base(query: str) -> dict:
    """Searches the knowledge base for relevant information.

    Args:
        query: The search query string.

    Returns:
        A dictionary containing matching knowledge base articles.
    """
    query_lower = query.lower()
    results = []
    for article in MOCK_KNOWLEDGE_BASE:
        if (
            query_lower in article["title"].lower()
            or query_lower in article["content"].lower()
            or query_lower in article["category"].lower()
        ):
            results.append(article)

    if results:
        return {"status": "success", "results": results, "count": len(results)}
    return {"status": "success", "results": [], "count": 0, "message": "No matching articles found."}


def analyze_sentiment(message: str) -> dict:
    """Analyzes the sentiment of a customer message.

    Args:
        message: The customer message to analyze.

    Returns:
        A dictionary with sentiment analysis results.
    """
    negative_keywords = ["angry", "frustrated", "terrible", "worst", "hate", "awful", "unacceptable", "furious"]
    urgent_keywords = ["urgent", "asap", "immediately", "emergency", "critical"]
    positive_keywords = ["thank", "great", "love", "excellent", "amazing", "happy", "satisfied"]

    message_lower = message.lower()

    neg_count = sum(1 for word in negative_keywords if word in message_lower)
    urg_count = sum(1 for word in urgent_keywords if word in message_lower)
    pos_count = sum(1 for word in positive_keywords if word in message_lower)

    if neg_count > 0 or urg_count > 0:
        sentiment = "negative"
        urgency = "high" if urg_count > 0 else "medium"
    elif pos_count > 0:
        sentiment = "positive"
        urgency = "low"
    else:
        sentiment = "neutral"
        urgency = "low"

    return {
        "sentiment": sentiment,
        "urgency": urgency,
        "escalation_recommended": urgency == "high",
    }
