const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Log all console messages
    page.on('console', msg => {
        fs.appendFileSync('browser_logs.txt', 'CONSOLE: ' + msg.text() + '\n');
    });
    page.on('pageerror', err => {
        fs.appendFileSync('browser_logs.txt', 'PAGE ERROR: ' + err.toString() + '\n');
    });

    try {
        await page.goto('http://localhost:8080', { waitUntil: 'networkidle0' });
        await page.click('a[href="#eda"]');
        await new Promise(r => setTimeout(r, 2000));
        await page.screenshot({path: 'debug_screenshot.png'});
    } catch (e) {
        fs.appendFileSync('browser_logs.txt', 'SCRIPT ERROR: ' + e.toString() + '\n');
    }

    await browser.close();
    console.log("Done. Check browser_logs.txt");
})();
