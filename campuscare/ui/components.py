from __future__ import annotations

from html import escape

import streamlit as st

from campuscare.constants import STATUS_LABELS
from campuscare.models import DonationItem, User


def brand(compact: bool = False) -> None:
    subtitle = "Student donation platform" if not compact else "NCI community"
    st.markdown(
        f"""
        <div class="cc-brand">
            <div class="cc-logo">C</div>
            <div>
                <div class="cc-brand-name">CampusCare</div>
                <div class="cc-brand-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, body: str, eyebrow: str = "CampusCare") -> None:
    st.markdown(
        f"""
        <section class="cc-hero">
            <span class="cc-eyebrow">{escape(eyebrow)}</span>
            <h1>{escape(title)}</h1>
            <p>{escape(body)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def status_pill(status: str) -> str:
    label = STATUS_LABELS.get(status, status.title())
    safe = escape(status)
    return f'<span class="cc-pill cc-status-{safe}">{escape(label)}</span>'


def item_summary_html(item: DonationItem) -> str:
    description = item.description
    if len(description) > 150:
        description = f"{description[:147]}..."
    donor_name = item.donor.full_name if item.donor else "NCI student"
    return f"""
    <div class="cc-card">
        <div>{status_pill(item.status)}<span class="cc-pill">{escape(item.category)}</span></div>
        <div class="cc-item-title">{escape(item.title)}</div>
        <div class="cc-muted">{escape(item.condition)} · Pickup: {escape(item.pickup_location)}</div>
        <p>{escape(description)}</p>
        <div class="cc-muted">Donated by {escape(donor_name)}</div>
    </div>
    """


def profile_header(user: User) -> None:
    course = escape(user.course or "Course not added")
    year = escape(user.year_of_study or "Year not added")
    st.markdown(
        f"""
        <div class="cc-profile-banner">
            <div class="cc-item-title" style="font-size:1.35rem;">{escape(user.full_name)}</div>
            <div class="cc-muted">{escape(user.email)}</div>
            <div style="margin-top:0.8rem;">{course} · {year}</div>
            <div style="margin-top:1rem;" class="cc-score">{user.trust_score}/100</div>
            <div class="cc-muted">Community trust score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
