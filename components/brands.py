"""Competitive Torpedoes - Brands included section."""
import streamlit as st
from db import get_platform_brands
from config import TOP_N
from components import section_header

_COLUMNS = 3


def render(comp_name: str, top_n=TOP_N):
    brands = get_platform_brands(comp_name, top_n)

    section_header(
        "\U0001F3F7️",
        "Brands Included",
        f"The {len(brands)} {comp_name} brands (ranked by LVI Score) "
        "whose metrics are averaged in this comparison",
    )

    if not brands:
        st.caption("Brand list unavailable — requires a database connection.")
        return

    with st.expander(f"{comp_name} — {len(brands)} brands", expanded=False):
        per_col = -(-len(brands) // _COLUMNS)
        cols = st.columns(_COLUMNS)
        for i, col in enumerate(cols):
            chunk = brands[i * per_col:(i + 1) * per_col]
            if chunk:
                col.markdown("\n".join(
                    f"{i * per_col + j + 1}. {name}"
                    for j, name in enumerate(chunk)
                ))
