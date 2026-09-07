from __future__ import annotations

from datetime import date, datetime
from typing import Literal, TypedDict
from uuid import uuid4

import streamlit as st


Priority = Literal["높음", "보통", "낮음"]


class Task(TypedDict):
    id: str
    title: str
    note: str
    priority: Priority
    due_date: str
    completed: bool
    created_at: str


PRIORITY_COLORS: dict[Priority, str] = {
    "높음": "#d95d39",
    "보통": "#d89b2b",
    "낮음": "#398a72",
}


def initialize_state() -> None:
    if "tasks" not in st.session_state:
        st.session_state.tasks = []


def add_task(title: str, note: str, priority: Priority, due_date: date) -> None:
    task: Task = {
        "id": uuid4().hex,
        "title": title.strip(),
        "note": note.strip(),
        "priority": priority,
        "due_date": due_date.isoformat(),
        "completed": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    st.session_state.tasks.insert(0, task)


def get_visible_tasks(tasks: list[Task], search: str, status: str, priority: str) -> list[Task]:
    normalized_search = search.strip().lower()
    visible_tasks: list[Task] = []

    for task in tasks:
        matches_search = not normalized_search or normalized_search in task["title"].lower()
        matches_status = (
            status == "전체"
            or (status == "진행 중" and not task["completed"])
            or (status == "완료" and task["completed"])
        )
        matches_priority = priority == "전체" or task["priority"] == priority
        if matches_search and matches_status and matches_priority:
            visible_tasks.append(task)

    return visible_tasks


def format_due_date(due_date: str) -> str:
    due = date.fromisoformat(due_date)
    today = date.today()
    if due < today:
        return "기한 지남"
    if due == today:
        return "오늘 마감"
    return f"{due.month}월 {due.day}일 마감"


def render_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap');

        :root {
            --ink: #20221f;
            --muted: #6d746c;
            --paper: #f5f4ed;
            --panel: #fffdf7;
            --line: #d9d9ce;
            --accent: #e6754a;
            --green: #398a72;
        }

        .stApp {
            background: var(--paper);
            color: var(--ink);
        }

        .block-container {
            max-width: 1120px;
            padding-top: 3.5rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            font-family: 'Manrope', sans-serif;
        }

        h1 {
            letter-spacing: -0.04em;
            font-weight: 800;
        }

        [data-testid="stSidebar"] {
            background: #e9ede5;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem;
        }

        .eyebrow {
            color: var(--accent);
            font-family: 'DM Mono', monospace;
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1.05rem;
            margin-top: -0.65rem;
            margin-bottom: 2rem;
        }

        .progress-track {
            background: #dedfd5;
            border-radius: 99px;
            height: 8px;
            overflow: hidden;
            margin: 0.55rem 0 1.8rem;
        }

        .progress-fill {
            background: var(--green);
            height: 100%;
            border-radius: inherit;
            transition: width 180ms ease;
        }

        .task-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-left: 4px solid var(--accent);
            border-radius: 4px;
            padding: 0.85rem 1rem 0.8rem;
            margin-bottom: 0.7rem;
        }

        .task-card.done {
            border-left-color: var(--green);
            opacity: 0.68;
        }

        .task-meta {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: -0.2rem;
        }

        .priority-label {
            font-family: 'DM Mono', monospace;
            font-size: 0.72rem;
            font-weight: 500;
        }

        .section-heading {
            color: var(--ink);
            font-size: 1.15rem;
            font-weight: 800;
            margin: 0.3rem 0 0.8rem;
        }

        div.stButton > button {
            border-radius: 3px;
            border: 1px solid var(--line);
            font-family: 'Manrope', sans-serif;
            font-weight: 700;
        }

        div.stButton > button[kind="primary"] {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
        }

        [data-testid="stForm"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 4px;
            padding: 1.15rem 1.2rem 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_task(task: Task) -> None:
    card_class = "task-card done" if task["completed"] else "task-card"
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    left, right = st.columns([0.08, 0.92], vertical_alignment="center")
    with left:
        completed = st.checkbox(
            "완료",
            value=task["completed"],
            key=f"complete_{task['id']}",
            label_visibility="collapsed",
        )
        if completed != task["completed"]:
            task["completed"] = completed
            st.rerun()
    with right:
        title = task["title"]
        if task["completed"]:
            st.markdown(f"~~**{title}**~~")
        else:
            st.markdown(f"**{title}**")
        details = [
            f"<span class='priority-label' style='color:{PRIORITY_COLORS[task['priority']]}'>{task['priority']} 우선순위</span>",
            format_due_date(task["due_date"]),
        ]
        if task["note"]:
            details.append(task["note"])
        st.markdown(f"<div class='task-meta'>{' · '.join(details)}</div>", unsafe_allow_html=True)
        if st.button("삭제", key=f"delete_{task['id']}"):
            st.session_state.tasks = [item for item in st.session_state.tasks if item["id"] != task["id"]]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar(tasks: list[Task]) -> tuple[str, str, str]:
    with st.sidebar:
        st.markdown("### 보기 설정")
        search = st.text_input("할 일 검색", placeholder="제목으로 검색")
        status = st.radio("상태", ["전체", "진행 중", "완료"], horizontal=True)
        priority = st.selectbox("우선순위", ["전체", "높음", "보통", "낮음"])
        st.divider()
        completed_count = sum(task["completed"] for task in tasks)
        st.caption(f"전체 {len(tasks)}개 · 완료 {completed_count}개")
        if completed_count and st.button("완료 항목 모두 삭제", use_container_width=True):
            st.session_state.tasks = [task for task in tasks if not task["completed"]]
            st.rerun()
    return search, status, priority


def main() -> None:
    st.set_page_config(page_title="오늘 할 일", page_icon="✓", layout="wide")
    render_styles()
    initialize_state()

    tasks: list[Task] = st.session_state.tasks
    search, status, priority = render_sidebar(tasks)

    st.markdown("<div class='eyebrow'>ONE PAGE / DAILY PLANNER</div>", unsafe_allow_html=True)
    st.title("오늘의 할 일")
    st.markdown("<p class='hero-copy'>해야 할 일을 선명하게 적고, 하나씩 가볍게 끝내보세요.</p>", unsafe_allow_html=True)

    total_count = len(tasks)
    completed_count = sum(task["completed"] for task in tasks)
    progress = completed_count / total_count if total_count else 0
    metric_one, metric_two, metric_three = st.columns(3)
    metric_one.metric("전체 할 일", f"{total_count}개")
    metric_two.metric("완료", f"{completed_count}개")
    metric_three.metric("진행률", f"{progress:.0%}")
    st.markdown(
        f"<div class='progress-track'><div class='progress-fill' style='width:{progress:.0%}'></div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-heading'>새 할 일 추가</div>", unsafe_allow_html=True)
    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("제목", placeholder="예: 발표 자료 초안 만들기")
        note = st.text_input("메모", placeholder="선택 사항")
        form_col_one, form_col_two, form_col_three = st.columns([1, 1, 0.75])
        with form_col_one:
            task_priority = st.selectbox("우선순위", ["높음", "보통", "낮음"], index=1)
        with form_col_two:
            due_date = st.date_input("마감일", value=date.today())
        with form_col_three:
            st.write("")
            st.write("")
            submitted = st.form_submit_button("할 일 추가", type="primary", use_container_width=True)
        if submitted:
            if not title.strip():
                st.warning("할 일 제목을 입력해 주세요.")
            else:
                add_task(title, note, task_priority, due_date)
                st.success("새 할 일을 추가했습니다.")

    st.markdown("<div class='section-heading' style='margin-top:2rem'>할 일 목록</div>", unsafe_allow_html=True)
    visible_tasks = get_visible_tasks(tasks, search, status, priority)
    if not visible_tasks:
        if tasks:
            st.info("조건에 맞는 할 일이 없습니다. 검색어나 필터를 바꿔보세요.")
        else:
            st.info("아직 등록된 할 일이 없습니다. 위에서 첫 할 일을 추가해 보세요.")
    else:
        for task in visible_tasks:
            render_task(task)


if __name__ == "__main__":
    main()
