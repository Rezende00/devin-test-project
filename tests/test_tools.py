import pytest

from customer_support_agent.tools import (
    analyze_sentiment,
    get_order_status,
    refund_order,
    search_knowledge_base,
)


class TestGetOrderStatus:
    def test_valid_order_returns_status(self):
        result = get_order_status("ORD-001")
        assert "status" in result
        assert result["status"] == "delivered"

    def test_valid_order_returns_all_fields(self):
        result = get_order_status("ORD-002")
        assert result["order_id"] == "ORD-002"
        assert result["customer_name"] == "Bob Smith"
        assert result["product"] == "USB-C Hub"
        assert result["status"] == "shipped"

    def test_invalid_order_returns_error(self):
        result = get_order_status("ORD-999")
        assert "error" in result

    def test_all_orders_accessible(self):
        for order_id in ["ORD-001", "ORD-002", "ORD-003", "ORD-004"]:
            result = get_order_status(order_id)
            assert "status" in result


class TestRefundOrder:
    def test_successful_refund(self):
        result = refund_order("ORD-001", reason="Changed my mind")
        assert result["status"] == "success"
        assert result["refund_amount"] == 79.99

    def test_cancelled_order_cannot_be_refunded(self):
        result = refund_order("ORD-004")
        assert result["status"] == "error"

    def test_invalid_order_id_handled_gracefully(self):
        result = refund_order("ORD-INVALID")
        assert "error" in result or result.get("status") == "error"

    def test_empty_order_id_handled_gracefully(self):
        result = refund_order("")
        assert "error" in result or result.get("status") == "error"


class TestSearchKnowledgeBase:
    def test_search_returns_results(self):
        result = search_knowledge_base("return")
        assert result["status"] == "success"
        assert result["count"] > 0

    def test_search_no_results(self):
        result = search_knowledge_base("xyznonexistent")
        assert result["count"] == 0

    def test_search_by_category(self):
        result = search_knowledge_base("policy")
        assert result["count"] >= 1

    def test_search_product_info(self):
        result = search_knowledge_base("headphones")
        assert result["count"] >= 1


class TestAnalyzeSentiment:
    def test_negative_sentiment(self):
        result = analyze_sentiment("I am so angry about this terrible service!")
        assert result["sentiment"] == "negative"

    def test_positive_sentiment(self):
        result = analyze_sentiment("Thank you, great service!")
        assert result["sentiment"] == "positive"

    def test_neutral_sentiment(self):
        result = analyze_sentiment("I want to check my order status")
        assert result["sentiment"] == "neutral"

    def test_urgent_detection(self):
        result = analyze_sentiment("This is urgent, I need help immediately!")
        assert result["urgency"] == "high"
        assert result["escalation_recommended"] is True

    def test_low_urgency_positive(self):
        result = analyze_sentiment("I love this product, amazing quality!")
        assert result["urgency"] == "low"
        assert result["escalation_recommended"] is False
