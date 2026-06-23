"""
할 일(To-Do) 관리 단일 페이지 앱
Streamlit 기반 간단한 작업 관리자
"""

import streamlit as st
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class TodoItem:
    """할 일 항목을 나타내는 데이터 클래스"""
    id: int
    title: str
    completed: bool
    created_at: str


def init_session_state() -> None:
    """세션 상태 초기화"""
    if "todos" not in st.session_state:
        st.session_state.todos: List[TodoItem] = []
    if "next_id" not in st.session_state:
        st.session_state.next_id: int = 1
    if "input_value" not in st.session_state:
        st.session_state.input_value: str = ""


def add_todo(title: str) -> None:
    """새로운 할 일 추가"""
    if title.strip():
        todo = TodoItem(
            id=st.session_state.next_id,
            title=title.strip(),
            completed=False,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        st.session_state.todos.append(todo)
        st.session_state.next_id += 1
        st.session_state.input_value = ""


def toggle_todo(todo_id: int) -> None:
    """할 일 완료 상태 토글"""
    for todo in st.session_state.todos:
        if todo.id == todo_id:
            todo.completed = not todo.completed
            break


def delete_todo(todo_id: int) -> None:
    """할 일 삭제"""
    st.session_state.todos = [
        todo for todo in st.session_state.todos if todo.id != todo_id
    ]


def get_todo_stats() -> tuple[int, int]:
    """완료 및 미완료 개수 반환"""
    completed = sum(1 for todo in st.session_state.todos if todo.completed)
    total = len(st.session_state.todos)
    return completed, total - completed


def render_summary() -> None:
    """할 일 요약 정보 표시"""
    completed, pending = get_todo_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("전체", completed + pending)
    with col2:
        st.metric("완료", completed)
    with col3:
        st.metric("미완료", pending)


def render_input_section() -> None:
    """할 일 입력 섹션 렌더링"""
    st.subheader("새로운 할 일 추가")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        title = st.text_input(
            "할 일 입력",
            value=st.session_state.input_value,
            placeholder="오늘 할 일을 입력하세요...",
            label_visibility="collapsed",
        )
    with col2:
        if st.button("추가", use_container_width=True):
            add_todo(title)
            st.rerun()


def render_todo_list() -> None:
    """할 일 목록 렌더링"""
    if not st.session_state.todos:
        st.info("아직 할 일이 없습니다. 새로운 할 일을 추가해보세요!")
        return
    
    st.subheader("할 일 목록")
    
    for todo in st.session_state.todos:
        col1, col2, col3, col4 = st.columns([0.5, 3, 1, 0.5])
        
        with col1:
            if st.checkbox(
                "✓",
                value=todo.completed,
                key=f"check_{todo.id}",
                label_visibility="collapsed",
            ):
                toggle_todo(todo.id)
                st.rerun()
        
        with col2:
            status = "✅" if todo.completed else "⭕"
            style = "text-decoration: line-through;" if todo.completed else ""
            st.markdown(
                f"{status} <span style='{style}'>{todo.title}</span>",
                unsafe_allow_html=True,
            )
        
        with col3:
            st.caption(todo.created_at)
        
        with col4:
            if st.button("🗑️", key=f"delete_{todo.id}", help="삭제"):
                delete_todo(todo.id)
                st.rerun()


def main() -> None:
    """메인 앱 함수"""
    st.set_page_config(
        page_title="할 일 관리",
        page_icon="✅",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    init_session_state()
    
    st.title("✅ 할 일 관리")
    
    render_summary()
    st.divider()
    
    render_input_section()
    st.divider()
    
    render_todo_list()


if __name__ == "__main__":
    main()
