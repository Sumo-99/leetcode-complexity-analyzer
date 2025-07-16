import { sampleFunction, scrapeFullCodeFromMonaco, testLCAnalysis } from '@src/sample-function';

console.log('[CEB] LC content script loaded');
console.log("Wommaleeee - LC Analysis");

// void testLCAnalysis();

scrapeFullCodeFromMonaco().then((res) => {
    // handle success if needed
    console.log('Scraping completed successfully', res);
}).catch((err) => {
    // handle error if needed
    console.error("Error in scraping: ", err);
});
