# 논리 ERD

기준: `common/models.py`, `neworld/models.py`의 **현재 모델 정의**와 최신 마이그레이션(`common` 0013, `neworld` 0025).  
`User`, `Group`은 Django 기본 인증 모델(`auth_user`, `auth_group`)이며, 현재 마이그레이션의 기본키는 Django가 생성한 정수형 `id` (`AutoField`)이다.

```mermaid
erDiagram
    USER ||--o| PROFILE : "프로필 보유"
    GROUP }o--o{ USER : "소속 사용자"

    USER o|--o{ QUESTION : "작성"
    GROUP o|--o{ QUESTION : "접근 그룹"
    USER }o--o{ QUESTION : "투표"
    QUESTION ||--o{ ANSWER : "답변"
    USER o|--o{ ANSWER : "작성"
    GROUP o|--o{ ANSWER : "접근 그룹"
    USER }o--o{ ANSWER : "투표"

    SCRIPTURE ||--o{ MEDITATION : "묵상 대상"
    USER o|--o{ MEDITATION : "작성"
    GROUP o|--o{ MEDITATION : "접근 그룹"
    USER }o--o{ MEDITATION : "투표"

    WEEKLY_BIBLE o|--o{ WB_SUMMARY : "주간 요약"
    BIBLE o|--o{ WB_SUMMARY : "성경 책"
    WEEKLY_BIBLE o|--o{ PUBS_INDEX : "출판물 색인"
    BIBLE o|--o{ PUBS_INDEX : "성경 책"
    WEEKLY_BIBLE o|--o{ RESEARCH : "연구"
    USER o|--o{ RESEARCH : "작성"
    GROUP o|--o{ RESEARCH : "접근 그룹"
    USER }o--o{ RESEARCH : "투표"

    USER o|--o{ CUSTOMER : "등록"
    GROUP o|--o{ CUSTOMER : "접근 그룹"
    USER }o--o{ CUSTOMER : "투표"
    CUSTOMER ||--o{ ACTIVITY : "활동 이력"
    USER o|--o{ ACTIVITY : "작성"
    GROUP o|--o{ ACTIVITY : "접근 그룹"
    USER }o--o{ ACTIVITY : "투표"

    USER o|--o{ COMMENT : "작성"
    GROUP o|--o{ COMMENT : "접근 그룹"
    QUESTION o|--o{ COMMENT : "댓글 대상"
    ANSWER o|--o{ COMMENT : "댓글 대상"
    MEDITATION o|--o{ COMMENT : "댓글 대상"
    RESEARCH o|--o{ COMMENT : "댓글 대상"
    CUSTOMER o|--o{ COMMENT : "댓글 대상"
    ACTIVITY o|--o{ COMMENT : "댓글 대상"

    USER o|--o{ GPT : "작성"
    GROUP o|--o{ GPT : "접근 그룹"
    USER }o--o{ GPT : "투표"
    GPT ||--o{ GPT_ANSWER : "응답"
    USER }o--o{ GPT_ANSWER : "투표"

    USER {
        integer id PK
        varchar username UK
        varchar email
        boolean is_staff
        boolean is_active
    }
    GROUP {
        integer id PK
        varchar name UK
    }
    PROFILE {
        integer id PK
        integer user_id FK_UK
        text bio NULL
        varchar website_url NULL
    }
    QUESTION {
        integer id PK
        integer author_id FK_NULL
        integer group_id FK_NULL
        varchar subject
        text content
        datetime create_date
        datetime modify_date NULL
    }
    ANSWER {
        integer id PK
        integer question_id FK
        integer author_id FK_NULL
        integer group_id FK_NULL
        text content
        datetime create_date
        datetime modify_date NULL
    }
    SCRIPTURE {
        integer id PK
        varchar scripture
        text bodytext
        varchar real_date
        varchar d_week NULL
        datetime create_date
    }
    MEDITATION {
        integer id PK
        integer scripture_id FK
        integer author_id FK_NULL
        integer group_id FK_NULL
        text meditation
        varchar real_date
        datetime create_date
        datetime modify_date NULL
    }
    WEEKLY_BIBLE {
        integer id PK
        integer year
        integer n_week
        varchar week
        varchar bible_range
        varchar bible_link NULL
        varchar specific_id NULL
        datetime create_date
    }
    BIBLE {
        integer id PK
        varchar bible_id
        varchar bible NULL
    }
    WB_SUMMARY {
        integer id PK
        integer weeklybible_id FK_NULL
        integer bible_id FK_NULL
        varchar chapter
        text bible_summary
        varchar specific_id NULL
        datetime create_date
    }
    PUBS_INDEX {
        integer id PK
        integer weeklybible_id FK_NULL
        integer bible_id FK_NULL
        varchar chapter
        varchar index_verse
        varchar pi_title
        varchar pi_link NULL
        varchar specific_id NULL
        datetime create_date
    }
    RESEARCH {
        integer id PK
        integer weeklybible_id FK_NULL
        integer author_id FK_NULL
        integer group_id FK_NULL
        text content
        datetime create_date
        datetime modify_date NULL
    }
    CUSTOMER {
        integer id PK
        integer author_id FK_NULL
        integer group_id FK_NULL
        text area NULL
        text name
        text keyman
        text position
        varchar grade
        text tel NULL
        text address NULL
        varchar email NULL
        text remark NULL
        datetime create_date
        datetime modify_date NULL
    }
    ACTIVITY {
        integer id PK
        integer customer_id FK
        integer author_id FK_NULL
        integer group_id FK_NULL
        text content
        datetime create_date
        datetime modify_date NULL
    }
    COMMENT {
        integer id PK
        integer author_id FK_NULL
        integer group_id FK_NULL
        integer question_id FK_NULL
        integer answer_id FK_NULL
        integer meditation_id FK_NULL
        integer research_id FK_NULL
        integer customer_id FK_NULL
        integer activity_id FK_NULL
        text content
        datetime create_date
        datetime modify_date NULL
    }
    GPT {
        integer id PK
        integer author_id FK_NULL
        integer group_id FK_NULL
        text content
        datetime create_date
        datetime modify_date NULL
    }
    GPT_ANSWER {
        integer id PK
        integer gpt_id FK
        text content
        datetime create_date
    }
```

## 관계 및 제약 요약

| 관계 | 카디널리티 | 삭제 동작 / 비고 |
|---|---|---|
| `User`–`Profile` | 1 : 0..1 | 사용자 생성 시 시그널로 Profile 생성. User 삭제 시 Profile 삭제(CASCADE). |
| `User`–`Group` | N : M | Django 기본 `auth_user_groups` 연결 테이블. |
| 작성자·그룹 연결 | 부모 1 : 자식 0..N | `Question`, `Answer`, `Meditation`, `Research`, `Customer`, `Activity`, `Comment`, `Gpt`의 FK는 nullable이며 CASCADE. |
| 투표자 연결 | `User` N : M 게시물 | `Question`, `Answer`, `Meditation`, `Research`, `Customer`, `Activity`, `Gpt`, `GptAnswer`별 자동 연결 테이블이 생성됨. |
| 콘텐츠 부모–자식 | 부모 1 : 자식 0..N | `Question`–`Answer`, `Scripture`–`Meditation`, `Customer`–`Activity`, `Gpt`–`GptAnswer`은 자식의 부모 FK가 필수이고 CASCADE. `WeeklyBible`/`Bible`에서 `WBsummary`·`PubsIndex`·`Research`로 향하는 FK는 선택 사항이다. |
| `Comment`–대상 | 대상 0..1 : 댓글 0..N | 대상 FK 6개 중 정확히 하나만 연결되도록 `comment_exactly_one_target` CHECK 제약을 둠. |

## 설계상 확인할 점

- `Comment`의 다중 nullable FK에는 정확히 하나의 대상만 허용하는 CHECK 제약이 적용돼 있다. 새로운 댓글 대상 유형을 추가할 때는 이 제약과 마이그레이션을 함께 갱신해야 한다.
- `voter = ManyToManyField(..., null=True)`의 `null=True`는 M:N 관계에서 실질적으로 사용되지 않으며, 빈 투표 집합은 연결 테이블에 행이 없는 상태로 표현된다.
- `WeeklyBible(year, n_week)`, `Scripture(real_date)`, `Bible(bible_id)`에는 각각 유니크 제약이 적용돼 있다. 운영 반영 전에는 중복 데이터 사전 점검이 필요하다.
