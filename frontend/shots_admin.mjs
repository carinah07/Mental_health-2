import { chromium } from 'playwright';
import fs from 'fs';

const OUT = 'D:/Careen/frontend/diagrams/screens';
fs.mkdirSync(OUT, { recursive: true });
const BASE = 'http://localhost:5173';

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 880 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();

const shot = async (name) => {
  await page.screenshot({ path: `${OUT}/${name}.png` });
  console.log('saved', name);
};

await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);
await shot('4_9_login');

await page.fill('input[type="text"]', 'admin');
await page.locator('input[type="password"]').first().fill('Admin@123');
await page.locator('button[type="submit"]').click();
await page.waitForURL('**/admin**', { timeout: 15000 });
await page.waitForTimeout(1000);
await shot('4_10_admin');

await browser.close();
console.log('DONE');
