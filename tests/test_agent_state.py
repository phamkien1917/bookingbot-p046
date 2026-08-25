from src.agents.state import create_initial_agent_state


def test_search_pool_survives_selected_property_turn() -> None:
    selected = [{"id": "selected", "title": "Căn 2"}]
    search_pool = [
        {"id": "first", "title": "Căn 1"},
        {"id": "selected", "title": "Căn 2"},
        {"id": "third", "title": "Căn 3"},
    ]
    state = create_initial_agent_state(
        session_id="session",
        query="so sánh căn này với căn 1",
        metadata={
            "chat_state": {
                "property_refs": selected,
                "search_result_refs": search_pool,
                "selected_property_id": "selected",
            }
        },
    )
    assert state["selected_properties"] == selected
    assert state["search_results"] == search_pool


def test_geo_preferences_are_restored() -> None:
    state = create_initial_agent_state(
        session_id="session",
        query="tiếp tục",
        metadata={
            "chat_state": {
                "commute_landmark": "Bệnh viện Bạch Mai",
                "max_commute_km": 5,
                "travel_mode": "WALK",
                "nearby_categories": ["school"],
            }
        },
    )
    assert state["max_commute_km"] == 5
    assert state["travel_mode"] == "WALK"
    assert state["nearby_categories"] == ["school"]
