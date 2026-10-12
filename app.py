"""GrowNote AI Agent 발표용 Streamlit 대시보드 — 가상 데이터 전용."""
import json
import streamlit as st
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from inventory_to_grownote import get_student_records

st.set_page_config(page_title="GrowNote AI Agent Demo", page_icon="📘", layout="wide")

@tool
def lookup_student_records(student_id: str) -> dict:
    """가상 학원 demo-academy의 학생 수업 기록을 읽기 전용으로 조회합니다. 학생 ID가 명확할 때만 호출합니다. 임의로 학생 ID나 기록을 만들지 마세요."""
    return get_student_records("demo-academy", student_id)

def run_agent(student_id):
    llm = ChatOllama(model="qwen3.5:2b", temperature=0)
    bound = llm.bind_tools([lookup_student_records])
    question = f"{student_id} 학생의 최근 수업 기록을 조회해 줘."
    messages = [HumanMessage(content=question)]
    first = bound.invoke(messages)
    calls = [{"name": c["name"], "args": c["args"]} for c in first.tool_calls]
    if not first.tool_calls:
        return question, calls, None, str(first.content), "도구를 호출하지 않았습니다."
    messages.append(first)
    results = []
    for call in first.tool_calls:
        if call["name"] != "lookup_student_records":
            result = {"error": "TOOL_NOT_ALLOWED"}
        else:
            try:
                result = lookup_student_records.invoke(call["args"])
            except Exception as exc:
                result = {"error": "INVALID_ARGUMENT", "detail": type(exc).__name__}
        results.append(result)
        messages.append(ToolMessage(content=json.dumps(result, ensure_ascii=False), tool_call_id=call["id"]))
    final = bound.invoke(messages)
    return question, calls, results[0] if results else None, str(final.content), None

st.title("📘 GrowNote AI Agent")
st.caption("2026-10-12 모두의연구소 AI Agent 과제 · Tool Calling 실시간 시연")
st.info("실제 학생 정보나 Supabase를 사용하지 않는 가상 데이터 실험입니다. 조회 전용이며 기록을 변경하지 않습니다.")

left, right = st.columns([1, 2])
with left:
    st.subheader("학생 조회")
    student_id = st.selectbox("테스트 학생 ID", ["STU-001", "STU-999"], format_func=lambda x: f"{x} — {'정상 조회' if x == 'STU-001' else '없는 학생 오류'}")
    run_clicked = st.button("🔎 AI 에이전트 실행", type="primary", use_container_width=True)
    st.caption("Ollama와 qwen3.5:2b가 설치되어 있어야 합니다.")
with right:
    st.subheader("실험 목표")
    st.markdown("**①** AI가 조회 도구를 선택하는가?  \\n**②** 도구가 실제 기록을 반환하는가?  \\n**③** 없는 학생에 대해 기록을 지어내지 않는가?")

if run_clicked:
    with st.spinner("Qwen3.5가 도구를 선택하고 답변을 생성하는 중입니다..."):
        try:
            question, calls, result, answer, warning = run_agent(student_id)
        except Exception as exc:
            st.error(f"실행 실패: {type(exc).__name__}: {exc}")
            st.info("Ollama 실행 상태와 설치 모델을 확인하세요: ollama list")
            st.stop()
    st.divider()
    st.subheader("실시간 실행 결과")
    st.write("**질문:**", question)
    if calls:
        st.success("AI가 조회 도구를 호출했습니다.")
    else:
        st.warning(warning or "도구 호출 없음")
    with st.expander("① 모델의 도구 호출", expanded=True):
        st.json(calls)
    with st.expander("② Python 조회 결과", expanded=True):
        if result is not None:
            st.json(result)
        else:
            st.write("도구 실행 결과 없음")
    st.subheader("③ AI 최종 답변")
    if result and result.get("error"):
        st.warning(f"조회 오류: {result['error']}")
    elif result:
        a, b = st.columns(2)
        a.metric("조회 기록", result.get("count", 0))
        b.metric("학생 ID", result.get("student_id", "-"))
        st.dataframe(result.get("records", []), use_container_width=True, hide_index=True)
    st.write(answer)
    st.caption("모델의 답변은 매 실행마다 달라질 수 있습니다. 위의 도구 결과와 비교하여 사실 여부를 확인하세요.")

st.divider()
st.caption("기존 과제 파일은 유지됩니다. 이 화면은 app.py로 추가된 발표용 인터페이스입니다.")
