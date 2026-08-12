# 맥주 계보 아카이브

일본 150년, 한국 90년 맥주 계보도. 연표가 아니라 **회사 혈통을 선으로 추적한 그림**이다 —
선이 모이면 합병, 갈라지면 분할.

**웹 페이지 → https://skda0228.github.io/beer/**

| | |
|---|---|
| 통합본 (일본 → 한국) | [`genealogy/beer-genealogy.html`](genealogy/beer-genealogy.html) |
| 일본 단독 | [`genealogy/jp-infographic.html`](genealogy/jp-infographic.html) |
| 한국 단독 | [`genealogy/kr-infographic.html`](genealogy/kr-infographic.html) |
| 자세한 설명 | [`genealogy/README.md`](genealogy/README.md) |

## GitHub Pages 켜기 (최초 1회)

배포 워크플로(`.github/workflows/pages.yml`)는 이미 있지만, Pages 사이트 자체를 만드는 것은
`GITHUB_TOKEN` 권한 밖이라 워크플로가 대신 켜줄 수 없다
(`Create Pages site failed. Resource not accessible by integration`).
저장소 **Settings → Pages → Build and deployment → Source** 를 **GitHub Actions** 로 한 번 바꾸면
그 뒤로는 푸시할 때마다 자동 배포된다.

브랜치 배포를 쓰려면 Source를 **Deploy from a branch**, 브랜치 `claude/google-notebook-mcp-6kj8ke`,
폴더 `/ (root)` 로 지정해도 된다. 루트에 `index.html`과 `.nojekyll`이 이미 있으므로 바로 뜬다.
이 경우 위 워크플로는 지워도 된다.

## 그 밖에

- [`NOTEBOOKLM_SETUP.md`](NOTEBOOKLM_SETUP.md) — NotebookLM MCP 설치·인증 안내
