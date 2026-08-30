# neworld
neworld.kr

## 의존성 관리

이 프로젝트는 [uv](https://docs.astral.sh/uv/)로 Python 의존성을 고정합니다.

```powershell
# 개발 의존성 동기화 및 Django 명령 실행
uv sync
uv run python manage.py runserver
```

운영 PostgreSQL 연결이 필요한 환경에서는 다음 그룹을 추가합니다.

```powershell
uv sync --group production
```

Celery 워커가 필요하면 다음 그룹을 추가합니다.

```powershell
uv sync --group worker
```
