"""Assignment Agent - Sale agent assignment and routing optimization."""

import json
import logging
from typing import Optional

from src.agents.state import AgentState, AgentType
from src.agents.tools.assignment_tools import (
    calculate_assignment_score,
    assign_sale_to_booking,
    get_available_sales,
)
from src.config import get_settings

logger = logging.getLogger(__name__)


async def assignment_agent(state: AgentState) -> dict:
    """Assignment agent - handles sale agent assignment.

    This agent:
    1. Calculates assignment scores for available sales
    2. Assigns the best matching sale to the booking
    3. Handles failover if assignment fails

    Args:
        state: Current agent state

    Returns:
        Updated state with assignment information
    """
    booking_id = state.get("booking_id")
    property_id = state.get("current_property_id")
    intent = state.get("intent")

    # Skip if no booking to assign
    if not booking_id:
        logger.info("No booking to assign, skipping assignment agent")
        return {
            "current_agent": AgentType.RESPOND,
        }

    try:
        # Step 1: Calculate scores for available sales
        score_result_str = calculate_assignment_score.invoke({
            "booking_id": booking_id,
        })
        score_result = json.loads(score_result_str)

        if "error" in score_result:
            logger.warning(f"Error calculating scores: {score_result['error']}")
            # Continue anyway with default assignment

        sale_rankings = score_result.get("sale_rankings", [])

        if not sale_rankings:
            # No sales available - trigger HITL
            logger.warning("No sales available for assignment")
            return {
                "awaiting_human": True,
                "hitl_reason": "NO_SALE_AVAILABLE",
                "hitl_context": {
                    "booking_id": booking_id,
                    "property_id": property_id,
                },
                "response": "Hiện tại không có sale nào sẵn sàng. Chúng tôi đang xử lý và sẽ liên hệ với bạn sớm nhất.",
            }

        # Step 2: Get top sale
        best_sale = sale_rankings[0]
        sale_id = best_sale.get("sale_id")
        sale_name = best_sale.get("sale_name")

        logger.info(f"Best sale for assignment: {sale_name} (score: {best_sale.get('total_score')})")

        # Step 3: Assign sale to booking
        assign_result_str = assign_sale_to_booking.invoke({
            "booking_id": booking_id,
            "sale_id": sale_id,
        })
        assign_result = json.loads(assign_result_str)

        if "error" in assign_result:
            logger.error(f"Error assigning sale: {assign_result['error']}")

            # Try failover - assign to next best sale
            if len(sale_rankings) > 1:
                next_sale = sale_rankings[1]
                logger.info(f"Trying failover with sale: {next_sale['sale_name']}")

                assign_result_str = assign_sale_to_booking.invoke({
                    "booking_id": booking_id,
                    "sale_id": next_sale.get("sale_id"),
                })
                assign_result = json.loads(assign_result_str)

                if "error" not in assign_result:
                    sale_name = next_sale.get("sale_name")

        if "error" in assign_result:
            # Assignment failed - trigger HITL
            return {
                "awaiting_human": True,
                "hitl_reason": "ASSIGNMENT_FAILED",
                "hitl_context": {
                    "booking_id": booking_id,
                    "property_id": property_id,
                    "error": assign_result["error"],
                    "top_sales": sale_rankings[:3],
                },
                "response": "Gặp sự cố khi phân công sale. Nhân viên của chúng tôi sẽ liên hệ với bạn để xác nhận.",
            }

        # Success!
        return {
            "analysis": f"Sale {sale_name} assigned to booking {state.get('booking_code', booking_id)}",
            "metadata": {
                **state.get("metadata", {}),
                "assignment": {
                    "sale_id": sale_id,
                    "sale_name": sale_name,
                    "score": best_sale.get("total_score"),
                    "all_candidates": sale_rankings,
                },
            },
            # Continue to RESPOND node
        }

    except Exception as e:
        logger.error(f"Error in assignment agent: {e}")

        # Trigger HITL on exception
        return {
            "awaiting_human": True,
            "hitl_reason": "ASSIGNMENT_ERROR",
            "hitl_context": {
                "booking_id": booking_id,
                "error": str(e),
            },
            "response": "Gặp lỗi trong quá trình xử lý. Chúng tôi sẽ liên hệ với bạn sớm nhất.",
            "error": str(e),
        }


async def get_top_sales_for_booking(
    booking_id: str,
    limit: int = 3,
) -> list[dict]:
    """Get top sales for a booking.

    Args:
        booking_id: Booking UUID
        limit: Number of top sales to return

    Returns:
        List of top sales with scores
    """
    try:
        result_str = calculate_assignment_score.invoke({
            "booking_id": booking_id,
        })
        result = json.loads(result_str)

        if "error" in result:
            return []

        return result.get("sale_rankings", [])[:limit]

    except Exception as e:
        logger.error(f"Error getting top sales: {e}")
        return []


async def reassign_booking(
    booking_id: str,
    new_sale_id: Optional[str] = None,
) -> dict:
    """Reassign a booking to a different sale.

    Args:
        booking_id: Booking UUID
        new_sale_id: New sale UUID (if None, will auto-select)

    Returns:
        Reassignment result
    """
    try:
        if not new_sale_id:
            # Get top sale excluding current assignment
            top_sales = await get_top_sales_for_booking(booking_id, limit=5)
            if top_sales:
                new_sale_id = top_sales[0].get("sale_id")

        if not new_sale_id:
            return {"error": "No available sale for reassignment"}

        result_str = assign_sale_to_booking.invoke({
            "booking_id": booking_id,
            "sale_id": new_sale_id,
            "force_assign": True,
        })
        result = json.loads(result_str)

        return result

    except Exception as e:
        logger.error(f"Error reassigning booking: {e}")
        return {"error": str(e)}
