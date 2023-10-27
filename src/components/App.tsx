import { FC, useEffect, useState } from 'react';
import useRecordQuestion from '../hooks/useRecordQuestion';

const App: FC = () => {
	const [isMicro, setIsMicro] = useState<boolean>(true);

	const [animNeznaika, setAnimNeznaika] = useState<string>('i_do_not_no_hello');
	const [durationAudio, setDurationAudio] = useState<number>(0);
	const [textRequest, setTextRequest] = useState<string>('');

	const [viewResponce, setViewResponce] = useState<boolean>(false);

	const { recording, startRecording, stopRecording, sendAudio } =
		useRecordQuestion();

	// const durationAnimate = lengthAudio => { TODO: ЕСЛИ ПОНАДОБИТЬСЯ ПОВТОРЯТЬ АНИМАЦИЮ
	// 	let repeatAnim = lengthAudio / 3;
	// 	console.log('durationAudio', lengthAudio);
	// 	console.log(repeatAnim);
	// 	return repeatAnim;
	// };

	// useEffect(() => {
	// 	durationAnimate(durationAudio);
	// }, [durationAudio]);

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
		const { audioBlob } = sendAudio();

		if (audioBlob) {
			const formData = new FormData();
			formData.append('audio', audioBlob);
			try {
				const response = await fetch(
					'https://n0fl3x.pythonanywhere.com/questions/',
					{
						method: 'POST',
						body: formData,
					}
				);
				const audioStream = response.body;

				const reader = audioStream.getReader();
				const audioChunks = [];

				while (true) {
					const { done, value } = await reader.read();

					if (done) {
						break;
					}

					audioChunks.push(value);
				}

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
						console.error(
							'Ошибка при получении длительности аудиофайла:',
							error
						);
					});
				/////
			} catch (error) {
				console.error('Ошибка при загрузке аудиофайла:', error);
			}
		}
	};

	const addText = async () => {
		try {
			const responce = await fetch(
				'https://n0fl3x.pythonanywhere.com/answers/example.mp3/'
			);
			const data = await responce.json();
			const text = data.text;
			setTextRequest(text);
		} catch (error) {
			console.log(error);
		}
	};

	const handleMicroClickStop = async () => {
		if (!isMicro) {
			await stopRecording();
			await receiveAudioStream();
			await addText();
			await playAudio(receivedAudioUrl);
			console.log('stop');
			setIsMicro(!isMicro);
		}
	};

	const handleMicroClickPlay = () => {
		if (isMicro) {
			startRecording();
			console.log('play');
			setIsMicro(!isMicro);
		}
	};

	useEffect(() => {
		if (!viewResponce) {
			setAnimNeznaika('i_do_not_no_hello');
		}
	}, [viewResponce]);

	return (
		<div className='wrapper__app'>
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
					<div
						className='app__micro_active'
						onClick={handleMicroClickStop}
					></div>
				)}
			</div>
		</div>
	);
};

export default App;
