# shared/utils.py
# Utility functions shared across all projects

import streamlit as st
import pandas as pd


def section_header(title: str, description: str = ""):
    """Renders a styled section header."""
    st.markdown(f"### {title}")
    if description:
        st.caption(description)
    st.markdown("---")


def metric_row(metrics: dict):
    """
    Renders a row of metric cards.

    Args:
        metrics: dict of {label: (value, delta)}
                 delta is optional → {label: value} also accepted
    """
    cols = st.columns(len(metrics))
    for col, (label, val) in zip(cols, metrics.items()):
        if isinstance(val, tuple):
            col.metric(label, val[0], val[1])
        else:
            col.metric(label, val)


def info_box(message: str, type: str = "info"):
    """Wrapper for st.info / st.success / st.warning / st.error."""
    getattr(st, type)(message)


def show_dataframe(df: pd.DataFrame, title: str = "", max_rows: int = 10):
    """Shows a styled dataframe with optional title."""
    if title:
        st.markdown(f"**{title}**")
    st.dataframe(df.head(max_rows), use_container_width=True)