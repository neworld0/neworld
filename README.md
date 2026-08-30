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

## 운영 환경 변수

운영 서버의 `.env`는 Git에 올리지 않습니다. PostgreSQL 설정과 함께 아래 값을 설정해야 합니다.

```dotenv
DJANGO_SECRET_KEY=<50자 이상의 무작위 비밀값>
DJANGO_DEBUG=False
```

`DJANGO_SECRET_KEY`는 Django의 세션·암호화 서명에 사용됩니다. 운영 설정은 이 값이 없으면 시작하지 않도록 구성되어 있습니다. `.env`를 `source`하지 말고, Django가 직접 읽게 두세요.
