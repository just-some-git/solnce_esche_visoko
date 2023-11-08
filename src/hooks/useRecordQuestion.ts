const useRecordQuestion = () => {
	const recognition = new (window.SpeechRecognition ||
		window.webkitSpeechRecognition)();

	recognition.lang = 'ru-RU';

	const startReq = () => {
		recognition.start();
	};

	const stopReq = () => {
		recognition.stop();
	};

	return { startReq, recognition, stopReq };
};

export default useRecordQuestion;
