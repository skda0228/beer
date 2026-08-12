// 2× PNG 내보내기 — Playwright(patchright) + 번들 Chromium
import { chromium } from '/opt/node22/lib/node_modules/notebooklm-mcp/node_modules/patchright/index.mjs';
const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const cwd = 'file://' + process.cwd() + '/';

for (const [src, out] of [
  ['jp-infographic.html', 'png/일본_맥주_계보_인포그래픽.png'],
  ['kr-infographic.html', 'png/한국_맥주_계보_인포그래픽.png'],
]) {
  const p = await br.newPage({ viewport:{width:1400,height:1000}, deviceScaleFactor:2 });
  await p.goto(cwd + src); await p.waitForTimeout(700);
  await p.locator('figure').first().screenshot({ path: out });
  await p.close(); console.log(out);
}

// 통합 페이지는 전체 스크롤 캡처
const p = await br.newPage({ viewport:{width:1400,height:1200}, deviceScaleFactor:2 });
await p.goto(cwd + 'beer-genealogy.html'); await p.waitForTimeout(900);
await p.screenshot({ path:'png/일본_한국_맥주_계보_통합.png', fullPage:true });
await p.close(); console.log('png/일본_한국_맥주_계보_통합.png');
await br.close();
