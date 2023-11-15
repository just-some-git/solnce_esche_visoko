import { useState } from 'react';
import useActualeDate from './useActualDate';

const useRequestQuestion = () => {
	const { actualDate } = useActualeDate();

	const [text, setText] = useState('');
	const [test, setTest] = useState(false);

	const [durationAudio, setDurationAudio] = useState<number>(0);
	const [textRequest, setTextRequest] = useState<string>('');

	let nameAudio;

	let receivedAudioUrl;

	const getAudioDuration = audioUrl => {
		return new Promise((resolve, reject) => {
			const audio = new Audio(audioUrl);
			audio.onloadedmetadata = () => {
				const duration = Math.floor(audio.duration * 1000);
				resolve(duration);
			};
			audio.onerror = error => {
				reject(error);
			};
		});
	};

	const receiveAudioStream = async () => {
		const formData = new FormData();
		nameAudio = actualDate();

		console.log(nameAudio);
		formData.append('name', nameAudio);
		formData.append('text', text);

		try {
			const response = await fetch(
				'https://n0fl3x.pythonanywhere.com/questions/',
				{
					method: 'POST',
					body: formData,
				}
			);
			const audioStream = response.body;

			// console.log('header', [...response.headers.entries()]); //перебор заголовков

			const reader = audioStream.getReader();
			const audioChunks = [];

			while (true) {
				const { done, value } = await reader.read();

				if (done) {
					break;
				}

				audioChunks.push(value);
			}

			console.log(audioChunks);
			const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
			const audioUrl = URL.createObjectURL(audioBlob);
			receivedAudioUrl = audioUrl;
			console.log('Аудиофайл успешно получен:', audioUrl);

			/////
			getAudioDuration(audioUrl)
				.then(duration => {
					console.log('Длительность аудиофайла:', duration, 'миллисекунд');
					setDurationAudio(duration);
				})
				.catch(error => {
					console.error('Ошибка при получении длительности аудиофайла:', error);
				});
			/////
		} catch (error) {
			console.error('Ошибка при загрузке аудиофайла:', error);
		}
	};

	const addText = async () => {
		try {
			const responce = await fetch(
				`https://n0fl3x.pythonanywhere.com/answers/${nameAudio}/`
			);
			const data = await responce.json();
			const text = data.text;
			setTextRequest(text);
		} catch (error) {
			console.log(error);
		}
	};

	return {
		receiveAudioStream,
		receivedAudioUrl,
		addText,
		text,
		setText,
		test,
		setTest,
		textRequest,
		durationAudio,
	};
};

export default useRequestQuestion;
