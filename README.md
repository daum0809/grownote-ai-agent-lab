# GrowNote AI 운영실장 — AI Agent 실습

**실습일:** 2026-10-12  
**프로젝트:** GrowNote 학생 학습기록 조회 에이전트

## 1. 프로젝트 목적

학원 강사가 작성한 학생의 수업 기록을 AI가 조회하고, 조회 결과를 자연어로 설명하는 에이전트의 작동 원리를 검증한다.

## 2. 사용 기술

- Python
- Ollama / Qwen3.5:2b
- LangChain / langchain-ollama
- Tool Calling
- 실행 기록(Trace) 및 오류 처리

## 3. 구현 기능

- 가상 학생 ID를 이용한 수업 기록 조회
- AI의 `lookup_student_records` 도구 선택 및 호출
- 조회 결과를 바탕으로 자연어 답변 생성
- 존재하지 않는 학생 ID에 대한 오류 처리

## 4. 실험 결과

**정상 조회:** `STU-001`

가상 학생의 수학 수업 기록 2건을 조회하고 답변 생성 확인.

**오류 조회:** `STU-999`

`STUDENT_NOT_FOUND`를 반환하고 학생 ID 확인을 안내함.

## 5. 실행 방법

```powershell
python inventory_to_grownote.py
```

가상 데이터 조회 함수 테스트.

```powershell
python grownote_ai_tool.py
```

Ollama를 이용한 AI 도구 호출 실험.

## 6. 안전 설계

- 조회 전용 기능 사용
- 실제 학생 개인정보 사용하지 않음
- 실제 Supabase 연결하지 않음
- 없는 학생 기록을 임의로 생성하지 않도록 오류 처리
- 도구 호출과 결과를 Trace 파일에 기록

## 7. 현재 한계 및 향후 개발

현재는 가상 데이터를 사용하는 로컬 실험이다. 실제 GrowNote 데이터베이스 연동, 인증 및 접근권한 검증, 운영 환경 테스트는 진행하지 않았다.

다음 단계는 Supabase 인증 및 RLS 정책을 점검하고 실제 학습 기록 조회 기능을 연결하는 것이다.

## 8. 실습 산출물

- `README.md`
- `design-packet.md`
- `inventory_to_grownote.py`
- `grownote_ai_tool.py`
- `my-agent/tool-definition.md`
- `my-agent/traces/trace-01.txt`
- `my-agent/traces/trace-02.txt`