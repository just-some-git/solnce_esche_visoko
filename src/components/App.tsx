import { FC, useEffect, useState } from 'react';
import useActualeDate from '../hooks/useActualDate';
import useRecordQuestion from '../hooks/useRecordQuestion';

const App: FC = () => {
	const [isMicro, setIsMicro] = useState<boolean>(true);

	const [animNeznaika, setAnimNeznaika] = useState<string>('i_do_not_no_hello');
	const [durationAudio, setDurationAudio] = useState<number>(0);
	const [textRequest, setTextRequest] = useState<string>('');

	let text = '';

	let nameAudio;

	const { actualDate } = useActualeDate();

	const [viewResponce, setViewResponce] = useState<boolean>(false);

	const { startReq, recognition, stopReq } = useRecordQuestion();

	useEffect(() => {
		console.log('use:', text);
	}, [text]);

	useEffect(() => {
		let anim = setTimeout(() => {
			// setAnimNeznaika('i_do_not_no_wait');
			setViewResponce(false);
		}, durationAudio);

		return () => {
			clearTimeout(anim);
		};
	}, [durationAudio]);

	let receivedAudioUrl;

	const playAudio = audioUrl => {
		const audio = new Audio(audioUrl);
		audio.play();
		setViewResponce(true);
		setAnimNeznaika('i_do_not_no');
	};

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
				'http://127.0.0.1:8000/questions/',
				{
					method: 'POST',
					body: formData,
				}
			);
			const audioStream = response.body;

			// console.log('header', [...response.headers.entries()]);

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
					console.log('Длительность аудиофайла:', duration, 'секунд');
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
				`http://127.0.0.1:8000/answers/${nameAudio}/`
			);
			const data = await responce.json();
			const text = data.text;
			setTextRequest(text);
		} catch (error) {
			console.log(error);
		}
	};

	// const handleMicroClickStop = async () => {
	// 	if (!isMicro) {
	// 		await stopReq();
	// 		await receiveAudioStream();
	// 		await addText();
	// 		await playAudio(receivedAudioUrl);
	// 		console.log('stop');
	// 		setIsMicro(!isMicro);
	// 	}
	// };

	const handleMicroClickPlay = () => {
		if (isMicro) {
			startReq();
			console.log('play');
			setIsMicro(false);
		}
	};

	useEffect(() => {
		if (!viewResponce) {
			setAnimNeznaika('i_do_not_no_hello');
		}
	}, [viewResponce]);

	recognition.onresult = async function (event) {
		const transcript = event.results[0][0].transcript;
		text = transcript;

		if (event.results[0].isFinal) {
			setIsMicro(true);
		}

		await receiveAudioStream();
		await addText();
		await playAudio(receivedAudioUrl);
	};

	return (
		<div className='wrapper__app'>
			<button
				onClick={() => {
					setAnimNeznaika('i_do_not_no');
					setTimeout(() => setAnimNeznaika('i_do_not_no_hello'), 3000);
				}}
			>
				кнопка 1
			</button>
			<button onClick={() => setAnimNeznaika('i_do_not_no_wait')}>
				кнопка 2
			</button>
			<button onClick={() => setAnimNeznaika('i_do_not_no_hello')}>
				кнопка 3
			</button>
			{!viewResponce ? (
				<img className='app__hello' src='./images/hello.png' alt='hello' />
			) : (
				<p className='text_answer'>{textRequest}</p>
			)}
			<div
				className='animation'
				style={{ animation: `${animNeznaika} 3s linear infinite` }}
			></div>

			<div className='block__app__micro'>
				{isMicro ? (
					<img
						className='app__micro'
						src='./images/micro.png'
						alt='micro'
						onClick={handleMicroClickPlay}
					/>
				) : (
					<div className='app__micro_active'></div>
				)}
			</div>
		</div>
	);
};

export default App;
