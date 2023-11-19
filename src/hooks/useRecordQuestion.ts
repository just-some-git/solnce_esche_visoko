const useRecordQuestion = () => {
	const recognition = new (window.SpeechRecognition ||
		window.webkitSpeechRecognition)();

	recognition.lang = 'ru-RU';

	const startReq = () => {
		recognition.start();
	};

	return { startReq, recognition };
};

export default useRecordQuestion;
