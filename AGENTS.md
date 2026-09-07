# Agent Instructions

## Repository Overview

- Streamlit으로 만드는 1페이지 MVP
- 순수 Python, 외부 DB 없음

## Working Guidelines

- Read the relevant existing documentation before editing it.
- Preserve the existing Markdown style and keep edits minimal.
- Do not add generated files or dependencies unless the task requires them.
- Do not commit changes unless explicitly requested.

## Setup Commands

-의존성 설치: pip install -r requirements.txt
-앱 실행: streamlit run app.py

## Code Style

-타입 힌트 사용, 함수는 작게 분리
-@st.cache_data 로 비용 큰 연산 캐싱
-UI 텍스트는 한국어

## Security

-API 키/시크릿은 코드에 하드코딩 금지
-비밀은 .streamlit/secrets.toml 또는 환경변수로

## Validation

After editing Markdown files, review the diff and verify that links, headings, and code blocks remain well formed.
