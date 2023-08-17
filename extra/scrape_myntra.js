const puppeteer = require('puppeteer');

async function scrapeMyntra() {
  try {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    const url = 'https://www.myntra.com/men-topwear';
    await page.goto(url);

    // Wait for the product information to load (adjust the time according to the website's loading speed)
    await page.waitForTimeout(5000);

    // Scrape the product information
    const productInfo = await page.evaluate(() => {
      const productElements = document.querySelectorAll('li.product-base');

      // Helper function to get the text content of an element
      const getText = (element, selector) => element.querySelector(selector)?.textContent.trim() || '';

      // Array to store the product information objects
      const products = [];

      // Iterate over each product element and extract the required information
      productElements.forEach(productElement => {
        const brand = getText(productElement, 'h3.product-brand');
        const productName = getText(productElement, 'h4.product-product');
        const price = getText(productElement, 'div.product-price span');

        // Create an object with the extracted information
        const productInfo = { brand, productName, price };
        products.push(productInfo);
      });

      return products;
    });

    console.log('Scraped product information:');
    console.log(productInfo);

    await browser.close();
  } catch (error) {
    console.error('Error:', error);
  }
}

scrapeMyntra();
