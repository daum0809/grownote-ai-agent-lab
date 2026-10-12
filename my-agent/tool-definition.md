# GrowNote 도구 정의서
## lookup_student_records (LLM 호출 도구 — 구현 완료)
- 역할: AI가 학생 ID를 받아 get_student_records 조회 함수를 호출
- 구현 환경: Ollama Qwen3.5:2b, LangChain
- 실패 처리: 학생 기록이 없으면 STUDENT_NOT_FOUND 반환
- 제한: 가상 데이터 조회 전용, 실제 DB 접근 및 수정 불가
## get_student_records (읽기 전용)
- 목적: 승인된 학원에서 특정 학생의 과거 수업 기록 조회
- 사용 시점: 이전 수업과 비교, 학습 변화 확인 요청
- 사용 금지: 학생 식별이 불확실하거나 요청자가 접근 권한이 없는 경우
- 입력: academy_id, student_id, limit (1~10)
- 출력: records 배열, 조회 건수, 조회 시각 또는 오류 코드
- 실패: STUDENT_NOT_FOUND, FORBIDDEN, INVALID_ARGUMENT
- 금지: 이름만으로 학생을 임의 확정하거나 기록을 만들어내지 않음

## save_lesson_record (쓰기 전용, 추후 구현)
- 목적: 강사가 작성한 수업 기록 저장
- 입력: academy_id, student_id, teacher_id, lesson_date, notes
- 조건: 로그인 및 역할 권한 검증, 입력 검증, 중복 방지
- 실행 전: 변경 대상과 내용을 표시하고 승인받음
- 실패: FORBIDDEN, INVALID_ARGUMENT, DUPLICATE_RECORD

## 안전 경계
- 모델이 요청한 academy_id를 신뢰하지 않고 서버 인증 정보와 대조
- DB 접근은 서버 측에서 RLS 및 역할 권한 적용
- 읽기와 쓰기 분리, 모든 실행 기록 남기기
- 학생 개인정보를 외부 LLM에 보내기 전에 최소화·가명화 검토
