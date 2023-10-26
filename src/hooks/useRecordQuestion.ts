import { useRef, useState } from 'react';

const useRecordQuestion = () => {
	const [recording, setRecording] = useState(false);
	const [audioChunks, setAudioChunks] = useState([]);
	const mediaRecorderRef = useRef(null);

	const startRecording = () => {
		if (!recording) {
			navigator.mediaDevices
				.getUserMedia({ audio: true })
				.then(stream => {
					const mediaRecorder = new MediaRecorder(stream);
					mediaRecorder.ondataavailable = e => {
						if (e.data.size > 0) {
							setAudioChunks([...audioChunks, e.data]);
						}
					};

					mediaRecorder.start();
					mediaRecorderRef.current = mediaRecorder;
					setRecording(true);
				})
				.catch(error =>
					console.error('Ошибка при доступе к микрофону:', error)
				);
		}
	};

	const stopRecording = () => {
		if (
			mediaRecorderRef.current &&
			mediaRecorderRef.current.state === 'recording'
		) {
			mediaRecorderRef.current.stop();
			setRecording(false);
		}
	};

	const sendAudio = () => {
		if (audioChunks.length > 0) {
			const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

			return { audioBlob, sendAudio: sendAudio };
		}
	};

	return { recording, startRecording, stopRecording, sendAudio };
};

export default useRecordQuestion;
