import React, { useState } from 'react';
import './App.scss';

function App() {
  const [inputText, setInputText] = useState('');
  const [sourceLanguage, setSourceLanguage] = useState('en-US');
  const [targetLanguage, setTargetLanguage] = useState('it-IT');
  const [translatedText, setTranslatedText] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const translateText = async () => {
    try {
      const response = await fetch('URL_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          'source-lang': sourceLanguage,
          'target-lang': targetLanguage,
        }),
      });

      if (!response.ok) {
        throw new Error('Something went wrong');
      }

      const data = await response.json();
      setTranslatedText(data.translation);
      setErrorMessage('');
    } catch (error) {
      console.error(error);
      setTranslatedText('');
      setErrorMessage('Error: Failed to translate text');
    }
  };

  return (
    <div className='App'>
      <header className='App-header'>
        <h1>Translate</h1>
      </header>
      <div className='Translator'>
        <div className='translateArea'>
          <select
            value={targetLanguage}
            onChange={e => setTargetLanguage(e.target.value)}
          >
            <option value='EN'>English</option>
            <option value='IT'>Italiano</option>
          </select>
          <textarea
            value={inputText}
            onChange={e => setInputText(e.target.value)}
            placeholder='Enter text to translate...'
          />
          <button onClick={translateText}>Translate</button>
        </div>
        <div className='TranslatedText'>
          <h2>Translated Text</h2>
          <textarea
            value={translatedText}
            readOnly
            placeholder='Translated text will appear here...'
          />
        </div>
      </div>
    </div>
  );
}

export default App;
