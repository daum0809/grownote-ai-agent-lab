"""GrowNote tool-calling lab: mock data only, no Supabase access."""
import json
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, HumanMessage
from langchain_ollama import ChatOllama
from inventory_to_grownote import get_student_records

@tool
def lookup_student_records(student_id: str) -> dict:
    """가상 학원 demo-academy의 학생 수업 기록을 읽기 전용으로 조회합니다. 학생 ID가 명확할 때만 사용하세요. 학생 ID를 추측하거나 생성하지 마세요. 없는 학생은 STUDENT_NOT_FOUND 오류를 반환합니다. 기록을 수정하거나 저장하지 않습니다."""
    return get_student_records('demo-academy', student_id)


def run(question):
    print('\n[질문]', question)
    llm = ChatOllama(model='qwen3.5:2b', temperature=0)
    bound = llm.bind_tools([lookup_student_records])
    messages = [HumanMessage(content=question)]
    first = bound.invoke(messages)
    print('[도구 호출]', [(x['name'], x['args']) for x in first.tool_calls])
    if not first.tool_calls:
        print('[도구 미호출] 모델 답변:', first.content)
        return
    messages.append(first)
    for call in first.tool_calls:
        if call['name'] != 'lookup_student_records':
            result = {'error': 'TOOL_NOT_ALLOWED'}
        else:
            try:
                result = lookup_student_records.invoke(call['args'])
            except Exception as exc:
                result = {'error': 'INVALID_ARGUMENT', 'detail': type(exc).__name__}
        print('[실행 결과]', json.dumps(result, ensure_ascii=False))
        messages.append(ToolMessage(content=json.dumps(result, ensure_ascii=False), tool_call_id=call['id']))
    final = bound.invoke(messages)
    print('[최종 답변]', final.content)

if __name__ == '__main__':
    run('STU-001 학생의 최근 수업 기록을 조회해 줘.')
    run('STU-999 학생의 최근 수업 기록을 조회해 줘.')
