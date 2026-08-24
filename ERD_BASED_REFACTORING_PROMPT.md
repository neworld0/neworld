# ERD 기반 Django 코드 개선 프롬프트

아래 프롬프트를 코딩 에이전트에게 그대로 전달하세요.

---

`LOGICAL_ERD.md`와 `PHYSICAL_ERD.md`를 기준으로 이 Django 프로젝트의 데이터 무결성을 개선해 주세요.

## 목표

현재 모델의 기능을 유지하면서 다음의 구조적 문제를 해결합니다.

1. 다형 댓글 구조(`Comment`)의 무결성 보장
2. 업무상 중복이 허용되지 않는 식별값의 중복 방지
3. M:N 투표 필드 선언의 불필요한 옵션 정리
4. 개발 SQLite와 운영 PostgreSQL에서 모두 안전하게 적용되는 마이그레이션 작성

## 반드시 먼저 할 일

1. `LOGICAL_ERD.md`, `PHYSICAL_ERD.md`, `common/models.py`, `neworld/models.py` 및 전체 마이그레이션을 읽습니다.
2. 작업 시작 전 `git status --short`로 기존 변경 사항을 확인하고, 본 작업과 관계없는 변경은 수정하거나 되돌리지 않습니다.
3. 현재 설치된 Django 버전과 `manage.py check`, 기존 테스트 결과를 확인합니다. 누락된 의존성이 있으면 어떤 패키지가 필요한지 보고하되, 승인 없이 애플리케이션 기능을 임의로 변경하지 않습니다.

## 구현 요구사항

### 1) `Comment` 대상 무결성

`neworld.Comment`는 아래 6개의 nullable FK 중 **정확히 하나**만 값이 있어야 합니다.

- `question`
- `answer`
- `meditation`
- `research`
- `customer`
- `activity`

`neworld/models.py`에 PostgreSQL과 SQLite 모두에서 동작하는 `models.CheckConstraint`를 추가해 이 규칙을 DB 레벨에서 강제하세요.

- `Q(...)` 조합으로 각 FK가 NULL이 아닌 경우의 수를 합산해 정확히 1인지 확인하는 조건을 사용합니다.
- 제약 이름은 의미 있고 30자 이내로 지정합니다. 예: `comment_exactly_one_target`.
- 기존 데이터가 제약을 위반할 수 있으므로, 마이그레이션 적용 전에 위반 행을 확인할 수 있는 ORM 또는 SQL 확인 방법을 문서화합니다.
- 데이터 정정·삭제는 수행하지 않습니다. 위반 데이터가 있는 경우에는 마이그레이션 적용 전에 중단하고, 건수와 식별자만 보고합니다.

### 2) 업무 식별값 유니크 제약

아래 제약을 `Meta.constraints`의 `models.UniqueConstraint`로 추가하세요.

| 모델 | 제약 컬럼 | 제약 이름 |
|---|---|---|
| `WeeklyBible` | `year`, `n_week` | `weeklybible_year_week_uniq` |
| `Scripture` | `real_date` | `scripture_real_date_uniq` |
| `Bible` | `bible_id` | `bible_bible_id_uniq` |

적용 전 중복 데이터 점검 쿼리(ORM과 PostgreSQL SQL 중 하나 이상)를 제공하세요. 중복 행을 자동 병합·삭제하지 마세요.

### 3) 투표 M:N 필드 정리

다음 `ManyToManyField`의 `null=True`를 제거하세요. M:N 관계에서 빈 관계는 조인 테이블 행이 없는 상태로 표현되므로 `null=True`는 DB 의미가 없습니다.

- `Question.voter`
- `Answer.voter`
- `Meditation.voter`
- `Research.voter`
- `Customer.voter`
- `Activity.voter`
- `Gpt.voter`
- `GptAnswer.voter`

`blank=True`는 추가하지 마세요. 현재 폼/관리자 화면의 입력 규칙은 불필요하게 변경하지 않는 것이 우선입니다.

### 4) 마이그레이션과 호환성

- 새 마이그레이션을 생성합니다. 기존 마이그레이션 파일은 수정하지 마세요.
- PostgreSQL 운영 DB와 SQLite 개발 DB에서 모두 적용 가능해야 합니다.
- 테이블명, 기존 FK, M:N 조인 테이블명, PK 타입(`AutoField`)은 변경하지 마세요.
- `on_delete=models.CASCADE`를 데이터베이스의 `ON DELETE CASCADE`로 바꾸는 작업은 범위에서 제외합니다. 기존 Django ORM 삭제 동작을 유지하세요.
- `GptAnswer`에 작성자 또는 그룹 FK를 새로 추가하지 마세요. 현재 ERD의 설계대로 `gpt`, `content`, `create_date`, `voter`만 유지합니다.

## 검증 요구사항

1. `python manage.py makemigrations --check --dry-run`으로 모델과 마이그레이션의 일치 여부를 확인합니다.
2. 빈 SQLite 테스트 DB에 대해 `python manage.py migrate`를 실행하고, 제약이 생성되는지 확인합니다.
3. `Comment`에 대상이 0개 또는 2개인 레코드를 저장할 때 `IntegrityError`가 발생하고, 정확히 1개인 경우 저장되는 테스트를 추가합니다.
4. 세 유니크 제약 각각에 대해 중복 INSERT가 `IntegrityError`가 되는 테스트를 추가합니다.
5. 기존 테스트 전체를 실행합니다.
6. PostgreSQL 서버에 직접 연결하거나 운영 DB에 마이그레이션을 적용하지 마세요. 운영 반영은 별도 승인 대상입니다.

## 결과 보고 형식

완료 후 아래를 간결하게 보고하세요.

1. 변경한 파일 목록과 핵심 변경
2. 생성한 마이그레이션 이름
3. 실행한 검증 명령과 결과
4. 제약 적용 전 운영 DB에서 실행해야 할 중복/무결성 사전 점검 SQL
5. 발견한 위험 또는 사용자 조치가 필요한 항목

---

## 운영 반영 전 PostgreSQL 사전 점검 SQL

아래 SQL은 읽기 전용 점검용입니다. 실제 스키마 이름이 기본 `public`이 아니면 테이블명을 조정하세요.

```sql
-- Comment: 댓글 대상이 0개이거나 2개 이상인 행
SELECT id,
       (question_id IS NOT NULL)::int
     + (answer_id IS NOT NULL)::int
     + (meditation_id IS NOT NULL)::int
     + (research_id IS NOT NULL)::int
     + (customer_id IS NOT NULL)::int
     + (activity_id IS NOT NULL)::int AS target_count
FROM neworld_comment
WHERE (question_id IS NOT NULL)::int
    + (answer_id IS NOT NULL)::int
    + (meditation_id IS NOT NULL)::int
    + (research_id IS NOT NULL)::int
    + (customer_id IS NOT NULL)::int
    + (activity_id IS NOT NULL)::int <> 1;

-- WeeklyBible: year + n_week 중복
SELECT year, n_week, COUNT(*) AS duplicate_count
FROM neworld_weeklybible
GROUP BY year, n_week
HAVING COUNT(*) > 1;

-- Scripture: real_date 중복
SELECT real_date, COUNT(*) AS duplicate_count
FROM neworld_scripture
GROUP BY real_date
HAVING COUNT(*) > 1;

-- Bible: bible_id 중복
SELECT bible_id, COUNT(*) AS duplicate_count
FROM neworld_bible
GROUP BY bible_id
HAVING COUNT(*) > 1;
```
