export const sampleFunction = () => {
  console.log('content script - sampleFunction() called from another module');
};

export const testLCAnalysis = () => {
  console.log('testLCAnalysis() called');
  const tabsetElement = document.querySelector('.flexlayout__tabset');
  if (tabsetElement) {
    console.log('Tabset content:', tabsetElement.textContent);
  } else {
    console.log('Element with class "flexlayout__tabset" not found.');
  }
};

export async function scrapeFullCodeFromMonaco() {
  console.log('[Extension] Waiting for Monaco editor to load...');

  const timeout = 15000; // 15 seconds
  const pollInterval = 100; // Check every 200ms
  const startTime = Date.now();

  // Wait loop for editor and at least one view-line to appear
  let editorLoaded = false;
  while (Date.now() - startTime < timeout) {
    const editorElement = document.querySelector('[class*="monaco-editor"]');
    const hasLines = editorElement?.querySelector('[class*="view-line"]');
    if (editorElement && hasLines) {
      console.log('[Extension] Monaco editor detected.');
      editorLoaded = true;
      break;
    }
    await new Promise(res => setTimeout(res, pollInterval));
  }
  if (!editorLoaded) {
    console.error('[Extension] Monaco editor did not load within timeout.');
    return;
  }

  // After timeout, check again
  const editorElement = document.querySelector('[class*="monaco-editor"]');
  const scrollContainer = editorElement?.querySelector('.overflow-guard');

  if (!editorElement || !scrollContainer) {
    console.error('[Extension] Monaco editor or scroll container not found after waiting.');
    alert("Could not find code editor. Please make sure you're on a LeetCode problem page.");
    return;
  }

  console.log('[Extension] Starting scroll-based scraping...');

  const totalHeight = scrollContainer.scrollHeight;
  const viewportHeight = scrollContainer.clientHeight;
  const scrollStep = viewportHeight / 2;
  const seenLines = new Set();

  for (let pos = 0; pos < totalHeight; pos += scrollStep) {
    scrollContainer.scrollTop = pos;
    await new Promise(res => setTimeout(res, 100));

    const codeLines = editorElement.querySelectorAll('[class*="view-line"]');
    console.log(`[Extension] Capturing ${codeLines.length} lines at scroll position ${pos}`);
    codeLines.forEach(line => {
      const text = line.textContent ? line.textContent.trim() : '';
      if (text !== '') seenLines.add(text);
    });
  }

  // Final sweep at bottom
  scrollContainer.scrollTop = totalHeight;
  await new Promise(res => setTimeout(res, 100));
  editorElement.querySelectorAll('[class*="view-line"]').forEach(line => {
    const text = line.textContent ? line.textContent.trim() : '';
    if (text !== '') seenLines.add(text);
  });

  const fullCode = Array.from(seenLines).join('\n');
  console.log('[Extension] Scraped full code:\n', fullCode);

  // TODO: Send fullCode to backend
}


