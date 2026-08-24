# 무결성 제약 적용 전 점검

대상 마이그레이션: `neworld.0026_alter_activity_voter_alter_answer_voter_and_more`.

운영 PostgreSQL에 이 마이그레이션을 적용하기 전에 아래 읽기 전용 SQL을 실행하세요. 결과가 하나라도 있으면 마이그레이션을 적용하지 말고, 표시된 `id` 또는 `ids`를 기준으로 데이터 정정 방안을 결정해야 합니다. 이 프로젝트는 해당 데이터를 자동 수정하거나 삭제하지 않습니다.

```sql
-- Comment: 대상 FK가 정확히 하나가 아닌 행
SELECT id,
       (question_id IS NOT NULL)::int + (answer_id IS NOT NULL)::int
     + (meditation_id IS NOT NULL)::int + (research_id IS NOT NULL)::int
     + (customer_id IS NOT NULL)::int + (activity_id IS NOT NULL)::int AS target_count
FROM neworld_comment
WHERE (question_id IS NOT NULL)::int + (answer_id IS NOT NULL)::int
    + (meditation_id IS NOT NULL)::int + (research_id IS NOT NULL)::int
    + (customer_id IS NOT NULL)::int + (activity_id IS NOT NULL)::int <> 1;

-- WeeklyBible: (year, n_week) 중복 행과 ID
SELECT year, n_week, array_agg(id ORDER BY id) AS ids
FROM neworld_weeklybible
GROUP BY year, n_week
HAVING COUNT(*) > 1;

-- Scripture: real_date 중복 행과 ID
SELECT real_date, array_agg(id ORDER BY id) AS ids
FROM neworld_scripture
GROUP BY real_date
HAVING COUNT(*) > 1;

-- Bible: bible_id 중복 행과 ID
SELECT bible_id, array_agg(id ORDER BY id) AS ids
FROM neworld_bible
GROUP BY bible_id
HAVING COUNT(*) > 1;
```

SQLite 개발 DB에서는 `array_agg` 대신 `group_concat(id)`를 사용합니다. 모든 결과가 비어 있음을 확인한 뒤에만 `python manage.py migrate`를 실행하세요.
