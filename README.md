# dnd-mentee-4th-5-backend

![](coverage.svg)

## 개요

DND 4기 5팀의 백엔드 프로젝트 입니다.

<br>

## 프로젝트 구조

기본적으로 DDD (Domain Driven Design) 아키텍처를 지향합니다.  
도메인 단위로 패키지를 나누고, 그 안에서 레이어 단위로 패키지를 나누었습니다.  
예를 들어 패키지 구조는 다음과 같습니다.

```
.
└── app
    ├── auth
    │   ├── application
    │   ├── domain
    │   └── external_interface
    ├── drinks
    │   ├── application
    │   ├── domain
    │   ├── external_interface
    │   └── infra_structure
    ├── health
    │   └── external_interface
    ├── reviews
    │   ├── application
    │   ├── domain
    │   ├── external_interface
    │   └── infra_structure
    ├── shared_kernel
    │   ├── application
    │   ├── domain
    │   ├── external_interface
    │   └── infra_structure
    ├── users
    │   ├── application
    │   ├── domain
    │   ├── external_interface
    │   └── infra_structure
    └── wishes
        ├── application
        ├── domain
        ├── external_interface
        └── infra_structure
└── tests
```

각 레이어 내부는 예를 들면 다음과 같습니다.

```
.
├── application
│   ├── dtos.py
│   └── service.py
├── domain
│   ├── entities.py
│   ├── repository.py
│   └── value_objects.py
├── external_interface
│   ├── json_dtos.py
│   └── routers.py
└── infra_structure
    ├── in_memory_repository.py
    ├── orm_models.py
    └── orm_repository.py

```

<br>

## 설치 방법

```bash
$ git clone https://github.com/dnd-mentee-4th/dnd-mentee-4th-5-backend.git
...

$ cd dnd-mentee-4th-5-backend.git
$ poetry install
```

<br>

## 실행 및 배포 방법

### 로컬에서 실행

올바른 실행을 위해 다음과 같이 환경 변수를 세팅해주세요.

```
JWT_SECRET_KEY = {JWT 에 사용할 SECRET KEY} 
JWT_ALGORITHM = {JWT 에 사용할 해시 알고리즘 이름}
DB_URL = {연결할 Postgres DB 의 SQLALCHEMY 커넥션 URL}
TEST_DB_URL = {연결할 Postgres 테스트용 DB 의 SQLALCHEMY 커넥션 URL}
```

예를 들면 다음과 같습니다.

```
JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS256"
DB_URL = "postgresql://root:1234@localhost:5432/coholy"
TEST_DB_URL = "postgresql://root:1234@localhost:5432/coholy_test"
```

다음처럼 `python` 커맨드로 실행 가능합니다.

```bash
$ python app/main.py
```

### 도커로 실행

다음 처럼 `docker` 빌드 후 컨테이너로 실행 가능합니다.

```bash
$ docker build -t coholy-backend-server .
$ docker run -d -p 8080:8080 \
-e JWT_SECRET_KEY = {JWT 에 사용할 SECRET KEY}  \
-e {JWT 에 사용할 해시 알고리즘 이름} \
-e DB_URL = {연결할 Postgres DB 의 SQLALCHEMY 커넥션 URL} \
coholy-backend-server 
```

<br>

---

## 개발 및 버저닝 규칙

### 패키지 의존성 관리

개발 과정에서는 [poetry](https://github.com/python-poetry/poetry)로 패키지를 관리합니다.  
다만 실제 운영에서 배포할 때는 `pip`와 `requirements.txt` 를 이용합니다.

```bash
# git clone 이후 필요한 패키지를 다운받습니다.
$ poetry install

# 필요한 패키지(ex. pandas, pytest)를 추가해야할 경우
$ poetry add pandas
$ poetry add pytest -D  # 개발 환경에서만 쓰이는 패키지로 추가하는 경우에 -D 옵션을 붙여줍니다.

# 배포를 위해 requirements.txt 를 만들어야하는 경우
$ poetry export -o requirements.txt --without-hashes
```

<br>

### Git Commit

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 규칙을 따릅니다.

```
fix: A bug fix. Correlates with PATCH in SemVer
feat: A new feature. Correlates with MINOR in SemVer
docs: Documentation only changes
style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
refactor: A code change that neither fixes a bug nor adds a feature
perf: A code change that improves performance
test: Adding missing or correcting existing tests
build: Changes that affect the build system or external dependencies (example scopes: pip, docker, npm)
ci: Changes to our CI configuration files and scripts (example scopes: GitLabCI)
```

커밋은 `git commit` 을 직접 사용하지 않고 다음처럼 [commitizen](https://github.com/commitizen-tools/commitizen) 을 사용합니다.

```bash
# commitzen 사용을 위해 가상환경 shell에 먼저 접속합니다.
$ poetry shell

# commitzen 을 사용한 커밋 과정 예시입니다.
$ (.venv) cz c
? Select the type of change you are committing  build: Changes that affect the build system or external dependencies (example scopes: pip, docker, npm)
? What is the scope of this change? (class or file name): (press [enter] to skip)

? Write a short and imperative summary of the code changes: (lower case and no period)
 poetry 관련 설정 초기화 및 commitizen, semantic-release 패키지 추가
? Provide additional contextual information about the code changes: (press [enter] to skip)

? Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer  No
? Footer. Information about Breaking Changes and reference issues that this commit closes: (press [enter] to skip)

build: poetry 관련 설정 초기화 및 commitizen, semantic-release 패키지 추가
```

이후 `git log` 를 통해 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 규칙대로 추가된 것을 확인할 수 있습니다.

```bash
$ (.venv) git log --oneline

b3929f1 (HEAD -> main) build: poetry 관련 설정 초기화 및 commitizen, semantic-release 패키지 추가
d55aa6a (origin/main, origin/HEAD) template update: ISSUE + PR (#2)
56b13b1 Initial commit
```

<br>

### Git Branch

브랜치는 다음과 같이 운영됩니다.

```
메인(main): 실제 서비스에 배포되어 운영되고 있는 코드입니다.
개발(develop): 아직 서비스에 배포되지는 않았지만, 다음 버전에 배포될 코드입니다.
기능(feature): 개발 브랜치에서 뻗어나와 개발해야될 기능을 담은 코드입니다.
```

특히 `feature` 브랜치 이름은 `feature/이슈 번호/작업 이름` 으로 만들어야 합니다.  
예를 들면, `feature/3/auth` 이런 식입니다.
작업할 때는 다음과 같은 플로우를 가지게 됩니다.

```bash
$ git switch develop
$ git switch -c feature/3/auth

코드 개발 및 커밋 작업 ..

$ git push origin feature/3/auth
```

### Pull Request

Pull Request와 Merge은 Github 상에서 이뤄집니다.

- PR 전에 관련 내용이 Issue 에 먼저 등록되어 있어야 합니다. Issue 가 없다면 이를 먼저 작성해주세요.
- PR 내용은 설정된 템플릿을 이용해주세요.
- PR 생성 후 Linked issued 에 관련된 이슈를 추가 해주세요.
- `feature` -> `develop` Merge 는 `Squash & Merge` 로 해주세요.
- `develop` -> `main` Merge 는 `Merge commits` 으로 해주세요.

Pull Request과 Merge의 흐름은 `feature` -> `develop` -> `main` 입니다.

<br>

---

## 팀 정보

- 팀 이름: 5조 - 5늘 술사줘
- 팀 내 역할

| Parts         | Name   |
| ------------- | ------ |
| Backend(조장) | 전시흠 |
| Backend       | 홍석준 |
| Frontend      | 이다예 |
| Frontend      | 김동영 |
| Design        | 이예나 |
| Design        | 최소은 |

<br>

## 관련 링크

- [프론트엔드](https://github.com/dnd-mentee-4th/dnd-mentee-4th-5-frontend)
- [백엔드](https://github.com/dnd-mentee-4th/dnd-mentee-4th-5-backend)
- [팀 노션](https://www.notion.so/330adbd74609421e89a9473e84a8204f)
