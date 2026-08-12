import { chromium } from '/opt/node22/lib/node_modules/notebooklm-mcp/node_modules/patchright/index.mjs';
const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await br.newPage({ viewport:{width:1400,height:1000}, colorScheme:'light', deviceScaleFactor:2 });
await p.goto('file://' + process.cwd() + '/jp-infographic.html');
await p.waitForTimeout(800);
await p.locator('figure').first().screenshot({ path:'일본_맥주_계보_인포그래픽.png' });
await p.close(); await br.close(); console.log('ok');
