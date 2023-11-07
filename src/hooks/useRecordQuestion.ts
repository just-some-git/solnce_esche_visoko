// import { useState } from 'react';

// const useRecordQuestion = () => {
// 	const [text, setText] = useState('');

// 	const recognition = new (window.SpeechRecognition ||
// 		window.webkitSpeechRecognition)();

// 	recognition.lang = 'ru-RU';

// 	recognition.onresult = function (event) {
// 		const result = event.results[0][0];

// 		if (result.isFinal) {
// 			setText(result.transcript);
// 			console.log('text:', result.transcript); // Вывести результат после обновления
// 		}
// 	};

// 	const startReq = () => {
// 		recognition.start();
// 		console.log('start');
// 	};

// 	return { startReq, text };
// };

// export default useRecordQuestion;

// import { useState } from 'react';

// const useRecordQuestion = () => {
// 	const [text, setText] = useState('');

// 	const recognition = new (window.SpeechRecognition ||
// 		window.webkitSpeechRecognition)();

// 	recognition.lang = 'ru-RU';

// 	const startReq = () => {
// 		recognition.start();
// 	};

// 	recognition.onresult = function (event) {
// 		const transcript = event.results[0][0].transcript;

// 		// console.log('text', transcript);

// 		console.log('text', text);
// 		setText(transcript);
// 	};

// 	return { startReq, text };
// };

// export default useRecordQuestion;

import { useEffect, useState } from 'react';

const useRecordQuestion = () => {
	const [text, setText] = useState('');

	const recognition = new (window.SpeechRecognition ||
		window.webkitSpeechRecognition)();

	recognition.lang = 'ru-RU';

	recognition.onresult = function (event) {
		const transcript = event.results[0][0].transcript;
		setText(transcript);
	};

	useEffect(() => {
		console.log('use:', text);
	}, [text]);

	const startReq = () => {
		recognition.start();
	};

	return { startReq, text };
};

export default useRecordQuestion;
