const puppeteer = require('puppeteer');

async function testPuppeteer() {
  try {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    const url = 'https://www.google.com/';
    await page.goto(url);

    console.log('Puppeteer is working properly! Headless browser opened successfully.');

    await browser.close();
  } catch (error) {
    console.error('Error:', error);
  }
}

testPuppeteer();
