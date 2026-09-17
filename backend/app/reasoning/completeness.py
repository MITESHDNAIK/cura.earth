"""
Strict sufficiency gate for multi-metric reasoning.

A response is allowed to reason only when at least three concrete
environmental signals are available. This prevents the recommendation
layer from inventing missing conditions.
"""

from typing import Any, Dict


def _leaf_count(profile: Dict[str, Any]) -> int:
    """
    Count concrete environmental observations.

    Each explicitly supplied environmental value counts as one signal.
    The what-if intervention itself does not count as baseline context.
    """

    count = 0

    for group, data in (profile or {}).items():
        if group == "what_if" or not isinstance(data, dict):
            continue

        for value in data.values():
            if value is not None and value != "":
                count += 1

    return count


def _groups(profile: Dict[str, Any]) -> set[str]:
    return {
        key
        for key, value in (profile or {}).items()
        if isinstance(value, dict)
        and value
        and key != "what_if"
    }


def _what_if(query: str) -> bool:
    q = (query or "").lower()

    return any(
        phrase in q
        for phrase in [
            "what if",
            "if i introduce",
            "if i add",
            "if i switch",
            "suppose i",
            "what happens if",
            "what would happen if",
        ]
    )


def assess_sufficiency(
    query: str,
    profile: Dict[str, Any] | None,
) -> Dict[str, Any]:

    profile = profile or {}
    q = (query or "").lower()

    leaves = _leaf_count(profile)
    groups = _groups(profile)
    is_what_if = _what_if(query)

    # ------------------------------------------------------------
    # WHAT-IF
    # ------------------------------------------------------------

    if is_what_if and leaves < 3:
        return {
            "sufficient": False,
            "requires_clarification": True,
            "missing": ["baseline_environment"],
            "groups": sorted(groups),
            "is_what_if": True,
            "clarification": (
                "Before I simulate that intervention, give me at least "
                "three baseline details such as soil carbon/moisture, "
                "rainfall, crop or land use, biodiversity, or habitat "
                "fragmentation."
            ),
        }

    # ------------------------------------------------------------
    # NO ENVIRONMENTAL INFORMATION
    # ------------------------------------------------------------

    if leaves == 0 and not groups:
        return {
            "sufficient": False,
            "requires_clarification": True,
            "missing": ["environmental_context"],
            "groups": [],
            "is_what_if": is_what_if,
            "clarification": (
                "Tell me about at least three environmental details — "
                "for example soil condition or SOC, rainfall/moisture, "
                "crop or land use, biodiversity, or habitat fragmentation."
            ),
        }

    # ------------------------------------------------------------
    # BIODIVERSITY-ONLY COMPLAINT
    # ------------------------------------------------------------

    biodiversity_only = (
        groups == {"biodiversity"}
        or ("biodiversity" in q and leaves <= 1)
    )

    if biodiversity_only:
        return {
            "sufficient": False,
            "requires_clarification": True,
            "missing": ["environmental_context"],
            "groups": sorted(groups),
            "is_what_if": is_what_if,
            "clarification": (
                "I can diagnose the biodiversity decline, but I don't "
                "want to guess its cause. What are the site's crop/"
                "land-use conditions and its water or soil conditions?"
            ),
        }

    # ------------------------------------------------------------
    # GENERAL THREE-SIGNAL REQUIREMENT
    # ------------------------------------------------------------

    if leaves < 3:
        missing_hint = "one or more environmental details"

        if "soil" not in groups:
            missing_hint = (
                "a soil detail such as SOC, pH, or moisture"
            )

        elif "climate" not in groups:
            missing_hint = (
                "a climate/water detail such as rainfall or moisture"
            )

        elif "land_use" not in groups:
            missing_hint = (
                "a land-use detail such as crop, management, or fragmentation"
            )

        return {
            "sufficient": False,
            "requires_clarification": True,
            "missing": ["more_environmental_context"],
            "groups": sorted(groups),
            "is_what_if": is_what_if,
            "clarification": (
                f"I have {leaves} usable environmental detail(s). "
                f"Give me {missing_hint} so I can connect at least "
                "three variables without inventing data."
            ),
        }

    # ------------------------------------------------------------
    # SUFFICIENT
    # ------------------------------------------------------------

    return {
        "sufficient": True,
        "requires_clarification": False,
        "missing": [],
        "groups": sorted(groups),
        "is_what_if": is_what_if,
        "clarification": None,
    }


def check_completeness(
    query: str,
    profile: Dict[str, Any] | None,
) -> Dict[str, Any]:
    return assess_sufficiency(query, profile)