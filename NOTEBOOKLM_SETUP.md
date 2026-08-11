# NotebookLM MCP 연결 가이드

맥주 노트북을 NotebookLM MCP로 붙이기 위한 설정입니다.
`.mcp.json`이 저장소 루트에 있으므로, 이 저장소를 연 Claude Code 세션은 자동으로 서버를 로드합니다.

## 패키지 정보

| 항목 | 값 |
|---|---|
| 패키지 | [`notebooklm-mcp`](https://www.npmjs.com/package/notebooklm-mcp) v2.0.0 |
| 저장소 | https://github.com/PleasePrompto/notebooklm-mcp |
| 라이선스 | MIT |
| 방식 | 공식 API 아님. Patchright(스텔스 Playwright 포크)로 **실제 Chrome을 구동**해 NotebookLM 웹을 조작 |
| 노출 도구 | 20개 (`ask_question`, `add_source`, `list_notebooks`, `generate_audio`, `download_audio` 등) |

## 사전 요구사항

- Node.js ≥ 18
- Chrome 스테이블 권장. 없으면 번들 Chromium 강제: `BROWSER_CHANNEL=chromium`
- **최초 1회 Google 로그인** — 눈에 보이는 Chrome 창이 떠야 함

## 설치

`.mcp.json`이 `npx notebooklm-mcp@latest`를 쓰므로 **별도 설치가 필요 없습니다.**
npx가 첫 실행 시 패키지를 받아 캐시하고, 이후 기동마다 `latest` 태그를 확인해 자동으로 최신을 따라갑니다.

버전을 고정하고 싶다면 전역 설치 후 `.mcp.json`을 아래로 바꾸세요:

```bash
npm install -g notebooklm-mcp@2.0.0
```

```json
{
  "mcpServers": {
    "notebooklm": { "command": "notebooklm-mcp", "args": [] }
  }
}
```

## 적용 범위 (scope)

`.mcp.json`은 **이 저장소에서만** 동작합니다. 다른 프로젝트에서도 쓰려면 user 스코프로 등록하세요:

```bash
claude mcp add --scope user notebooklm -- npx notebooklm-mcp@latest
```

| 스코프 | 저장 위치 | 적용 범위 |
|---|---|---|
| `local` (기본) | `~/.claude.json` → `projects[<cwd>].mcpServers` | 해당 디렉터리, 본인만 |
| `project` | 저장소 루트 `.mcp.json` | 이 저장소를 체크아웃한 모든 사람 |
| `user` | `~/.claude.json` → 최상위 `mcpServers` | **본인의 모든 프로젝트** |

등록 확인: `claude mcp list`

이 설정들은 모두 **Claude Code CLI 전용**입니다.
claude.ai 웹·데스크톱 앱의 커넥터는 별개 체계이며, stdio 서버를 직접 등록할 수 없습니다
(원격 HTTP 엔드포인트만 받습니다 — 아래 참고).

## 최초 인증 (로컬 머신에서만 가능)

1. 로컬 Claude Code에서 이 저장소를 연다
2. `setup_auth` 도구를 호출한다 → Chrome 창이 뜬다
3. 창에서 본인 Google 계정(skda00228@gmail.com)으로 직접 로그인한다
4. 쿠키가 사용자별 Chrome 프로필에 저장된다 → 이후 실행은 헤드리스로 자동 재사용

인증 확인: `get_health` → `"authenticated": true`

## 사용 흐름

```
setup_auth              # 최초 1회
list_notebooks          # 노트북 목록
add_notebook            # 맥주 노트북을 라이브러리에 등록 (NotebookLM URL 필요)
select_notebook         # 활성 노트북 지정
ask_question            # 노트북 근거 기반 질의 (인용 포함)
```

## 원격/컨테이너 환경에서 동작하지 않는 이유

Claude Code 웹·클라우드 세션(이 저장소가 클론된 환경)에서는 **인증을 완료할 수 없습니다**:

1. **대화형 로그인 불가** — `setup_auth`는 사람이 직접 타이핑해야 하는 Google 로그인 창을 띄웁니다.
   컨테이너에는 `DISPLAY`가 없고, `xvfb-run`으로 가상 디스플레이를 만들어도 화면을 볼 수도 입력할 수도 없습니다.
2. **컨테이너 휘발성** — 로그인에 성공하더라도 세션 종료 시 Chrome 프로필이 함께 사라져 매번 재인증이 필요합니다.
3. **세션 중 MCP 로드 불가** — Claude Code는 시작 시점에 MCP 서버를 읽습니다.
   실행 중인 세션에 설정을 추가해도 재시작 전까지는 도구가 나타나지 않습니다.

따라서 **로컬 데스크톱 Claude Code에서 사용하세요.**

## claude.ai 웹·데스크톱 앱에서 쓰려면

claude.ai의 커넥터는 stdio가 아니라 **원격 HTTP MCP 엔드포인트**만 받습니다.
`notebooklm-mcp` v2.0.0은 Streamable-HTTP 전송을 지원하므로 이론상 가능하지만,
서버를 공개 주소에 노출해야 합니다 — 그 서버는 로그인된 Google 세션을 쥐고 있으므로
인증 없이 공개하면 안 됩니다. 개인 용도라면 로컬 Claude Code CLI 사용을 권합니다.

## 보안 참고

이 서버는 서드파티 패키지이며, 로그인한 Google 계정 세션 쿠키를 로컬 Chrome 프로필에 보관한 채 브라우저를 자동 조작합니다.
해당 세션은 NotebookLM뿐 아니라 같은 계정의 Gmail·Drive 등에도 유효한 자격 증명입니다.
전용 계정을 쓰거나, 최소한 어떤 계정으로 로그인하는지 의식하고 쓰는 편이 안전합니다.

## 대안 — Google Drive 커넥터

NotebookLM 노트북의 원본 소스가 Drive에 있다면, 이미 연결된 Google Drive MCP로 직접 읽을 수 있습니다.
브라우저 자동화도, 별도 인증도 필요 없습니다. 맥주 자료의 경우 Drive의 `맥주` 폴더에 원본이 모두 있습니다.
