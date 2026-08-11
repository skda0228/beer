import { chromium } from '/opt/node22/lib/node_modules/notebooklm-mcp/node_modules/patchright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const jobs = [
  ['jp-beer-genealogy.html', 0, '일본_맥주_계보도_1870-2026.png'],
  ['kr-beer-genealogy.html', 0, '한국_맥주_계보도_1933-2026.png'],
  ['kr-beer-genealogy.html', 1, '한국_수제맥주_흥망_2013-2023.png'],
];
for (const [file, idx, out] of jobs) {
  const p = await b.newPage({ viewport:{width:1400,height:1000}, colorScheme:'light', deviceScaleFactor:2 });
  await p.goto('file://' + process.cwd() + '/' + file);
  await p.waitForTimeout(600);
  const fig = p.locator('figure').nth(idx);
  await fig.screenshot({ path: out });
  await p.close();
  console.log('wrote', out);
}
await b.close();
