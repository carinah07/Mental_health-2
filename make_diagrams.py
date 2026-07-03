# -*- coding: utf-8 -*-
"""
Generates the six design diagrams for the MindCare report as PNG images.
Reflects: JWT authentication, admin user management, downloadable reports,
three instruments (PHQ-9, GAD-7, SDQ), AI feedback, Mia assistant.
"""

import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch,
    Rectangle,
    Ellipse,
    FancyArrowPatch,
    Polygon,
    Circle,
)

OUT = r"d:\Careen\frontend\diagrams"
os.makedirs(OUT, exist_ok=True)

TEAL = "#0d685c"
TEAL_LIGHT = "#e6fff9"
GREY = "#666666"
ACCENT = "#1f9d8c"


def new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", path)


def box(ax, x, y, w, h, text, fc=TEAL_LIGHT, ec=TEAL, fs=9, bold=False, round=True):
    if round:
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=2.0",
            linewidth=1.5, edgecolor=ec, facecolor=fc,
        )
    else:
        patch = Rectangle((x, y), w, h, linewidth=1.5, edgecolor=ec, facecolor=fc)
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h / 2, text, ha="center", va="center",
        fontsize=fs, fontweight="bold" if bold else "normal", color="#13332f", wrap=True,
    )


def ellipse(ax, x, y, w, h, text, fc="white", ec=TEAL, fs=8):
    ax.add_patch(Ellipse((x, y), w, h, linewidth=1.4, edgecolor=ec, facecolor=fc))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color="#13332f")


def arrow(ax, p1, p2, color=TEAL, style="-|>", lw=1.4, ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            p1, p2, arrowstyle=style, mutation_scale=14,
            linewidth=lw, color=color, linestyle=ls,
            shrinkA=2, shrinkB=2,
        )
    )


def line(ax, p1, p2, color=GREY, lw=1.2, ls="-"):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=lw, linestyle=ls)


def actor(ax, x, y, label):
    r = 2.2
    ax.add_patch(Circle((x, y + 8), r, fill=False, edgecolor=TEAL, linewidth=1.6))
    line(ax, (x, y + 8 - r), (x, y + 1), color=TEAL, lw=1.6)
    line(ax, (x - 3, y + 5), (x + 3, y + 5), color=TEAL, lw=1.6)
    line(ax, (x, y + 1), (x - 3, y - 4), color=TEAL, lw=1.6)
    line(ax, (x, y + 1), (x + 3, y - 4), color=TEAL, lw=1.6)
    ax.text(x, y - 8, label, ha="center", va="center", fontsize=9,
            fontweight="bold", color=TEAL)


def title(ax, text):
    ax.text(50, 98, text, ha="center", va="top", fontsize=13,
            fontweight="bold", color=TEAL)


def use_case():
    fig, ax = new_ax(13, 10)
    title(ax, "Figure 3.1  Use Case Diagram")

    ax.add_patch(Rectangle((24, 6), 52, 84, linewidth=1.6, edgecolor=TEAL,
                           facecolor="#f7fffd"))
    ax.text(50, 87, "MindCare Mental Health System",
            ha="center", va="center", fontsize=10, fontweight="bold", color=TEAL)

    actor(ax, 8, 68, "Registered\nUser")
    actor(ax, 8, 28, "Parent /\nGuardian")
    actor(ax, 92, 68, "Administrator")
    actor(ax, 92, 28, "AI Provider\n(LLM)")

    cases = [
        (32, 78, "Register /\nLogin"),
        (52, 78, "Take PHQ-9 /\nGAD-7"),
        (32, 64, "Complete SDQ\n(Child)"),
        (52, 64, "Chat with Mia"),
        (32, 50, "Receive AI\nFeedback"),
        (52, 50, "Download\nReport"),
        (32, 36, "Submit Follow-up\nReferral"),
        (52, 36, "Manage Users"),
        (32, 22, "Generate User\nReports"),
    ]
    for x, y, t in cases:
        ellipse(ax, x, y, 16, 8.5, t)

    for tgt in [(32, 78), (52, 78), (52, 64), (32, 50), (52, 50), (32, 36)]:
        line(ax, (10, 68), (tgt[0] - 8, tgt[1]), color=GREY)
    for tgt in [(32, 64), (32, 50), (32, 36)]:
        line(ax, (10, 28), (tgt[0] - 8, tgt[1]), color=GREY)
    for tgt in [(52, 36), (32, 22)]:
        line(ax, (90, 68), (tgt[0] + 8, tgt[1]), color=ACCENT)
    line(ax, (90, 28), (52 + 8, 64), color=ACCENT, ls="--")
    line(ax, (90, 28), (32 + 8, 50), color=ACCENT, ls="--")

    save(fig, "usecase.png")


def activity():
    fig, ax = new_ax(7.5, 14)
    title(ax, "Figure 3.2  Activity Diagram \u2013 Assessment & Report")

    cx = 50
    ax.add_patch(Circle((cx, 94), 1.8, color=TEAL))
    steps = [
        (86, "Login / Register\n(JWT token)"),
        (77, "Select assessment\n(PHQ-9 / GAD-7 / SDQ)"),
        (68, "Enter age group & sex"),
        (59, "Answer current item"),
    ]
    for y, t in steps:
        box(ax, cx - 18, y - 3.5, 36, 7, t)
    arrow(ax, (cx, 92.2), (cx, 89.5))
    arrow(ax, (cx, 82.5), (cx, 80.5))
    arrow(ax, (cx, 73.5), (cx, 71.5))
    arrow(ax, (cx, 64.5), (cx, 62.5))

    dec = [(cx, 51), (cx + 13, 45), (cx, 39), (cx - 13, 45)]
    ax.add_patch(Polygon(dec, closed=True, edgecolor=TEAL, facecolor="#fff7e6", linewidth=1.5))
    ax.text(cx, 45, "More\nitems?", ha="center", va="center", fontsize=9)
    arrow(ax, (cx, 55.5), (cx, 51.2))
    arrow(ax, (cx + 13, 45), (cx + 26, 45), color=ACCENT)
    line(ax, (cx + 26, 45), (cx + 26, 59), color=ACCENT)
    arrow(ax, (cx + 26, 59), (cx + 18, 59), color=ACCENT)
    ax.text(cx + 27.5, 52, "yes", fontsize=8.5, color=ACCENT)

    after = [
        (31, "Compute total score"),
        (22, "Store record linked\nto user account"),
        (13, "Generate AI feedback (LLM)"),
        (4, "Display score & feedback"),
    ]
    for y, t in after:
        box(ax, cx - 18, y - 3.5, 36, 7, t)
    ax.text(cx - 4.5, 40, "no", fontsize=8.5, color=TEAL)
    arrow(ax, (cx, 39), (cx, 34.5))
    arrow(ax, (cx, 27.5), (cx, 25.5))
    arrow(ax, (cx, 18.5), (cx, 16.5))
    arrow(ax, (cx, 9.5), (cx, 7.5))

    box(ax, cx + 16, 1, 30, 7, "Download report\n(.docx)", fc="#fff7e6")
    box(ax, cx - 46, 1, 30, 7, "Offer follow-up\n(if elevated)", fc="#fff7e6")
    arrow(ax, (cx + 18, 4), (cx + 16, 4), color=ACCENT)
    arrow(ax, (cx - 18, 4), (cx - 16, 4), color=ACCENT)

    save(fig, "activity.png")


def sequence():
    fig, ax = new_ax(14, 9)
    title(ax, "Figure 3.3  Sequence Diagram \u2013 Authenticated Assessment")

    actors = [
        (8, "User"),
        (26, "Vue UI"),
        (48, "Django API"),
        (70, "Database"),
        (90, "AI Provider"),
    ]
    top, bottom = 84, 10
    for x, name in actors:
        box(ax, x - 7, top, 14, 5, name, fc=TEAL_LIGHT, fs=8, bold=True)
        line(ax, (x, top), (x, bottom), color=GREY, ls="--")

    def msg(x1, x2, y, text, ret=False):
        arrow(ax, (x1, y), (x2, y), color=(GREY if ret else TEAL),
              ls=("--" if ret else "-"))
        midx = (x1 + x2) / 2
        ax.text(midx, y + 1.2, text, ha="center", va="bottom", fontsize=7.5,
                color="#13332f")

    msg(8, 26, 78, "Login credentials")
    msg(26, 48, 73, "POST /api/auth/login/")
    msg(48, 26, 68, "JWT access token", ret=True)
    msg(8, 26, 63, "Complete assessment")
    msg(26, 48, 58, "POST /api/assessment/ + Bearer token")
    msg(48, 70, 53, "INSERT record (user_id)")
    msg(70, 48, 48, "OK", ret=True)
    msg(48, 90, 43, "Request AI feedback")
    msg(90, 48, 38, "Generated feedback", ret=True)
    msg(48, 26, 33, "score + feedback + report id", ret=True)
    msg(26, 8, 28, "Display + download option", ret=True)

    save(fig, "sequence.png")


def class_box(ax, x, y, w, name, attrs, methods):
    line_h = 3.8
    n_attr = len(attrs)
    n_meth = len(methods)
    head_h = 5.5
    attr_h = max(line_h * n_attr + 2, 5)
    meth_h = max(line_h * n_meth + 2, 5)
    ax.add_patch(Rectangle((x, y + attr_h + meth_h), w, head_h,
                           edgecolor=TEAL, facecolor=TEAL, linewidth=1.4))
    ax.text(x + w / 2, y + attr_h + meth_h + head_h / 2, name, ha="center",
            va="center", fontsize=9, fontweight="bold", color="white")
    ax.add_patch(Rectangle((x, y + meth_h), w, attr_h, edgecolor=TEAL,
                           facecolor="white", linewidth=1.4))
    for i, a in enumerate(attrs):
        ax.text(x + 1.2, y + meth_h + attr_h - 2.5 - i * line_h, a, ha="left",
                va="center", fontsize=7.2, color="#13332f")
    ax.add_patch(Rectangle((x, y), w, meth_h, edgecolor=TEAL,
                           facecolor="#f7fffd", linewidth=1.4))
    for i, m in enumerate(methods):
        ax.text(x + 1.2, y + meth_h - 2.5 - i * line_h, m, ha="left",
                va="center", fontsize=7.2, color="#13332f")


def classes():
    fig, ax = new_ax(14, 10)
    title(ax, "Figure 3.4  Class Diagram")

    class_box(ax, 2, 58, 24, "User",
              ["- username: str", "- email: str", "- is_staff: bool"],
              ["+ authenticate()", "+ is_admin()"])
    class_box(ax, 2, 28, 24, "SelfAssessment",
              ["- user_id: FK", "- score: int", "- ai_response: str",
               "- severity_level: str"],
              ["+ save()", "+ generate_report()"])
    class_box(ax, 30, 24, 24, "ChildAssessment",
              ["- user_id: FK", "- difficulties: int", "- ai_response: str"],
              ["+ save()", "+ generate_report()"])
    class_box(ax, 58, 40, 22, "ModelConfig",
              ["- name, provider", "- temperature"],
              ["+ build_client()"])
    class_box(ax, 84, 40, 14, "FeatureModel\nAssignment",
              ["- feature_key", "- model: FK"],
              ["+ get_client()"])

    arrow(ax, (14, 58), (14, 52), color=TEAL)
    ax.text(15, 55, "1  *", fontsize=8, color=TEAL)
    arrow(ax, (14, 28), (42, 38), color=TEAL)
    arrow(ax, (26, 45), (30, 40), color=TEAL)

    save(fig, "classes.png")


def node3d(ax, x, y, w, h, text, fc=TEAL_LIGHT):
    d = 3
    ax.add_patch(Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d),
                          (x + w, y + h)], closed=True, edgecolor=TEAL,
                         facecolor="#cdeee7", linewidth=1.3))
    ax.add_patch(Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d),
                          (x + w, y + h)], closed=True, edgecolor=TEAL,
                         facecolor="#cdeee7", linewidth=1.3))
    ax.add_patch(Rectangle((x, y), w, h, edgecolor=TEAL, facecolor=fc, linewidth=1.4))
    ax.text(x + w / 2, y + h - 3, text, ha="center", va="top", fontsize=9,
            fontweight="bold", color="#13332f")


def deployment():
    fig, ax = new_ax(13, 8.5)
    title(ax, "Figure 3.5  Deployment Diagram")

    node3d(ax, 6, 46, 26, 30, "<<device>>\nClient Device")
    box(ax, 9, 50, 20, 7, "Web Browser\nVue 3 SPA (Vite)", fc="white", fs=8)

    node3d(ax, 40, 34, 30, 42, "<<server>>\nApplication Server")
    box(ax, 43, 58, 24, 6, "Nginx (web server)", fc="white", fs=8)
    box(ax, 43, 49, 24, 6, "Gunicorn", fc="white", fs=8)
    box(ax, 43, 40, 24, 6, "Django REST API\n(JWT Auth)", fc="white", fs=8)

    node3d(ax, 80, 50, 18, 22, "<<db>>\nDatabase")
    box(ax, 82, 53, 14, 6, "PostgreSQL", fc="white", fs=8)

    node3d(ax, 80, 12, 18, 22, "<<external>>\nAI Provider")
    box(ax, 82, 15, 14, 6, "LLM API", fc="white", fs=8)

    arrow(ax, (32, 55), (40, 55), style="<|-|>", color=TEAL)
    ax.text(36, 57, "HTTPS", ha="center", fontsize=8, color=TEAL)
    arrow(ax, (70, 56), (80, 58), style="<|-|>", color=TEAL)
    arrow(ax, (64, 40), (86, 26), style="<|-|>", color=ACCENT, ls="--")

    save(fig, "deployment.png")


def entity(ax, x, y, w, name, rows):
    line_h = 3.6
    head_h = 5
    body_h = line_h * len(rows) + 2
    ax.add_patch(Rectangle((x, y + body_h), w, head_h, edgecolor=TEAL,
                           facecolor=TEAL, linewidth=1.4))
    ax.text(x + w / 2, y + body_h + head_h / 2, name, ha="center", va="center",
            fontsize=8, fontweight="bold", color="white")
    ax.add_patch(Rectangle((x, y), w, body_h, edgecolor=TEAL, facecolor="white",
                           linewidth=1.4))
    for i, (key, field) in enumerate(rows):
        yy = y + body_h - 2.8 - i * line_h
        if key:
            ax.text(x + 1, yy, key, ha="left", va="center", fontsize=6.5,
                    fontweight="bold", color=ACCENT)
        ax.text(x + 7, yy, field, ha="left", va="center", fontsize=6.5,
                color="#13332f")


def erd():
    fig, ax = new_ax(14, 10)
    title(ax, "Figure 3.6  Entity Relationship Diagram (ERD)")

    entity(ax, 2, 62, 24, "auth_user",
           [("PK", "id"), ("", "username"), ("", "email"),
            ("", "is_staff"), ("", "date_joined")])
    entity(ax, 30, 58, 28, "self_assessment",
           [("PK", "id"), ("FK", "user_id"), ("", "assessment_type"),
            ("", "score"), ("", "ai_response"), ("", "severity_level"),
            ("", "created_at")])
    entity(ax, 30, 22, 28, "child_assessment",
           [("PK", "id"), ("FK", "user_id"), ("", "difficulties"),
            ("", "prosocial"), ("", "score"), ("", "ai_response"),
            ("", "created_at")])
    entity(ax, 62, 40, 24, "model_config",
           [("PK", "id"), ("", "name"), ("", "provider")])
    entity(ax, 62, 8, 28, "feature_model_assignment",
           [("PK", "id"), ("FK", "model_id"), ("", "feature_key")])

    arrow(ax, (26, 70), (30, 72), style="-|>", color=TEAL)
    ax.text(27, 74, "1 *", fontsize=7.5, color=TEAL)
    arrow(ax, (26, 70), (30, 38), style="-|>", color=TEAL)
    arrow(ax, (74, 40), (76, 22), style="-|>", color=TEAL)

    save(fig, "erd.png")


if __name__ == "__main__":
    use_case()
    activity()
    sequence()
    classes()
    deployment()
    erd()
    print("All diagrams generated in", OUT)
