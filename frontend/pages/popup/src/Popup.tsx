import '@src/Popup.css';
import { t } from '@extension/i18n';
import { PROJECT_URL_OBJECT, useStorage, withErrorBoundary, withSuspense } from '@extension/shared';
import { exampleThemeStorage } from '@extension/storage';

import React, { useState, useEffect } from 'react';

import { cn, ErrorDisplay, LoadingSpinner, ToggleButton } from '@extension/ui';

const notificationOptions = {
  type: 'basic',
  iconUrl: chrome.runtime.getURL('icon-34.png'),
  title: 'Injecting content script error',
  message: 'You cannot inject script here!',
} as const;


const Popup = () => {

  const { isLight } = useStorage(exampleThemeStorage);
  const logo = isLight ? 'popup/logo_vertical.svg' : 'popup/logo_vertical_dark.svg';


  // State for analysis results
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  // Send message to content script to trigger analysis
  const handleAnalyzeClick = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id!, { type: 'SCRAPE_AND_ANALYZE' });
    });
  };

  // Listen for analysis results from background/content scripts
  useEffect(() => {
    const listener = (message: any, sender: any, sendResponse: any) => {
      if (message.type === 'ANALYSIS_RESULT') {
        setAnalysisResult(message.result);
      }
    };
    chrome.runtime.onMessage.addListener(listener);
    return () => {
      chrome.runtime.onMessage.removeListener(listener);
    };
  }, []);

  const goGithubSite = () => chrome.tabs.create(PROJECT_URL_OBJECT);

  const injectContentScript = async () => {
    const [tab] = await chrome.tabs.query({ currentWindow: true, active: true });

    if (tab.url!.startsWith('about:') || tab.url!.startsWith('chrome:')) {
      chrome.notifications.create('inject-error', notificationOptions);
    }

    await chrome.scripting
      .executeScript({
        target: { tabId: tab.id! },
        files: ['/content-runtime/example.iife.js', '/content-runtime/all.iife.js'],
      })
      .catch(err => {
        // Handling errors related to other paths
        if (err.message.includes('Cannot access a chrome:// URL')) {
          chrome.notifications.create('inject-error', notificationOptions);
        }
      });
  };

  return (
    <div className={cn('App', isLight ? 'bg-slate-50' : 'bg-gray-800')}>
      <header className={cn('App-header', isLight ? 'text-gray-900' : 'text-gray-100')}>
        <button onClick={goGithubSite}>
          <img src={chrome.runtime.getURL(logo)} className="App-logo" alt="logo" />
        </button>
        <p>
          Edit <code>pages/popup/src/Popup.tsx</code>
        </p>
        <button
          className={cn(
            'mt-4 rounded px-4 py-1 font-bold shadow hover:scale-105',
            isLight ? 'bg-blue-200 text-black' : 'bg-gray-700 text-white',
          )}
          onClick={injectContentScript}>
          {t('injectButton')}
        </button>
        <button
          className={cn(
            'mt-4 rounded px-4 py-1 font-bold shadow hover:scale-105',
            isLight ? 'bg-green-400 text-black' : 'bg-green-700 text-white',
          )}
          onClick={handleAnalyzeClick}
        >
          Analyze Code
        </button>
        <ToggleButton>{t('toggleTheme')}</ToggleButton>
        <div>{t("testString")}</div>
        {/* Analysis Results Section */}
        <div className="mt-6 p-4 rounded bg-white text-black shadow max-w-lg mx-auto">
          <h2 className="font-bold mb-2">Analysis Results</h2>
          {analysisResult ? (
            <pre className="whitespace-pre-wrap text-sm">
              {JSON.stringify(analysisResult, null, 2)}
            </pre>
          ) : (
            <span className="text-gray-500">No results yet.</span>
          )}
        </div>
      </header>
    </div>
  );
};

export default withErrorBoundary(withSuspense(Popup, <LoadingSpinner />), ErrorDisplay);
