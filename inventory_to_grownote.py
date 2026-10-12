"""수업의 inventory_tool.py를 GrowNote 조회 도구로 변형한 오프라인 실습.
실제 Supabase에 연결하지 않으며, 개인정보가 없는 가상 데이터만 사용합니다.
"""
import json

MOCK_RECORDS = {
    ('demo-academy', 'STU-001'): [
        {'lesson_date': '2026-09-28', 'subject': '수학', 'notes': '분수 연산 복습'},
        {'lesson_date': '2026-10-12', 'subject': '수학', 'notes': '분수 응용문제 풀이'},
    ]
}

def get_student_records(academy_id: str, student_id: str, limit: int = 5) -> dict:
    """승인된 학원의 학생 기록을 읽기 전용으로 조회합니다. 학생 ID가 불명확하면 조회하지 않습니다."""
    if academy_id != 'demo-academy':
        return {'error': 'FORBIDDEN'}
    if not isinstance(limit, int) or not 1 <= limit <= 10 or not student_id:
        return {'error': 'INVALID_ARGUMENT'}
    records = MOCK_RECORDS.get((academy_id, student_id))
    if records is None:
        return {'error': 'STUDENT_NOT_FOUND'}
    return {'student_id': student_id, 'count': len(records[-limit:]), 'records': records[-limit:]}

if __name__ == '__main__':
    for student_id in ['STU-001', 'STU-999']:
        print(json.dumps(get_student_records('demo-academy', student_id), ensure_ascii=False))
