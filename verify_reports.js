const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const files = [
    'index.html',
    'cto_insight.html',
    'developer_practice.html'
  ];

  for (const file of files) {
    const filePath = 'file://' + path.resolve('output/tech-daily', file);
    await page.goto(filePath);
    await page.screenshot({ path: '/home/jules/verification/screenshots/v2_' + file.replace('.html', '.png') });
    console.log('Verified ' + file);
  }

  await browser.close();
})();
