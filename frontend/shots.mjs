import { chromium } from 'playwright';
import fs from 'fs';

const OUT = 'D:/Careen/frontend/diagrams/screens';
fs.mkdirSync(OUT, { recursive: true });
const BASE = 'http://localhost:5173';

const feedbackMd = `**Thank you for completing the assessment.** Your responses suggest a **moderate** level of depressive symptoms (a score of 14 out of 27).

This does not define you, and it is a helpful starting point for taking care of yourself:

- Keep a gentle daily routine for sleep, meals and a little movement.
- Reach out to one person you trust and share how you have been feeling.
- Notice small positive moments each day, however minor they seem.

If these feelings continue for more than two weeks or become heavier, please consider speaking with a counsellor or health worker. You are not alone, and support is available.`;

const miaReply = `I'm really glad you reached out, and I hear you. Feeling stressed about exams is completely understandable.

Let's take this one step at a time. Could you tell me which part feels most overwhelming right now? While we talk, try a slow breath with me: in for 4 seconds, hold for 4, and out for 6. You're doing the right thing by talking about it.`;

async function mock(page) {
  await page.route('**/api/assessment/phq9/**', r =>
    r.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ score: 14, response: feedbackMd, redirect_link: '/followup/1' }) }));
  await page.route('**/ask_akili/**', r =>
    r.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ response: miaReply }) }));
  await page.route('**/api/chatbot/**', r =>
    r.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ response: miaReply }) }));
}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 880 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();
await mock(page);

const shot = async (name) => { await page.screenshot({ path: `${OUT}/${name}.png` }); console.log('saved', name); };

// 1. Landing page
await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.main-title');
await page.waitForTimeout(2500);
await shot('4_1_landing');

// 2. Mental Health dashboard
await page.goto(BASE + '/mental-health', { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.heading');
await page.waitForTimeout(800);
await shot('4_2_dashboard');

// 3. Assessment selection modal
await page.locator('.grid .card').first().click();
await page.waitForSelector('.modal .intro-form');
await page.waitForTimeout(600);
await shot('4_3_selection');

// 4. PHQ-9 question screen
await page.locator('.modal .intro-form button').first().click(); // depression
await page.waitForSelector('.modal select');
await page.locator('.modal select').nth(0).selectOption('21-25');
await page.locator('.modal select').nth(1).selectOption('Male');
await page.locator('.modal .intro-form button').first().click(); // start assessment
await page.waitForSelector('.modal .options button');
await page.waitForTimeout(600);
await shot('4_4_question');

// 5. Score + AI feedback
const picks = [2, 2, 2, 2, 2, 2, 2, 0, 0]; // sums to 14 (moderate), matches AI feedback text
for (let i = 0; i < 9; i++) {
  await page.locator('.modal .options button').nth(picks[i]).click();
  await page.waitForTimeout(300);
}
await page.waitForSelector('.ai-response', { timeout: 15000 });
await page.waitForTimeout(900);
await shot('4_5_feedback');

// 6. Mia chat
await page.goto(BASE + '/mental-health', { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.heading');
await page.locator('.grid .card').nth(1).click(); // Chat with Mia card
await page.waitForSelector('.chat-body');
await page.waitForTimeout(500);
await page.locator('textarea').fill('I feel really stressed about my exams');
await page.locator('.send-btn').click();
await page.waitForTimeout(1500);
await shot('4_6_chat');

// 7. Follow-up referral form
await page.goto(BASE + '/followup/1', { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.modal .intro-form');
await page.locator('input').nth(0).fill('+255 7XX XXX XXX');
await page.locator('input').nth(1).fill('Dar es Salaam, Tanzania');
await page.locator('textarea').fill('I would like to speak with a counsellor about ongoing stress and low mood.');
await page.waitForTimeout(500);
await shot('4_7_followup');

// 8. Swahili (Kiswahili) interface
await page.goto(BASE + '/mental-health', { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.lang-switch select');
await page.selectOption('.lang-switch select', 'sw');
await page.waitForTimeout(700);
await shot('4_8_swahili');

await browser.close();
console.log('ALL DONE');
