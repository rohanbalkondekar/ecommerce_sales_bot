const puppeteer = require('puppeteer');

async function scrapeAmazon() {
  try {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    const searchQuery = 'laptop'; // Change this to any product you want to search for
    const url = `https://www.amazon.com/s?k=${encodeURIComponent(searchQuery)}`;
    await page.goto(url);

    // Wait for the search results to load (adjust the time according to the website's loading speed)
    await page.waitForSelector('[data-asin]', { timeout: 5000 });

    // Scrape product titles and prices
    const products = await page.evaluate(() => {
      const results = [];
      const productElements = document.querySelectorAll('[data-asin]');
      productElements.forEach((element) => {
        const titleElement = element.querySelector('h2');
        const priceElement = element.querySelector('.a-price .a-offscreen');

        const title = titleElement ? titleElement.textContent.trim() : 'Title not available';
        const price = priceElement ? priceElement.textContent : 'Price not available';

        results.push({ title, price });
      });
      return results;
    });

    console.log('Scraped products:');
    console.log(products);

    await browser.close();
  } catch (error) {
    console.error('Error:', error);
  }
}

scrapeAmazon();

