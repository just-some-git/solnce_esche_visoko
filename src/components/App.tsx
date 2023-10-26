import { FC, useEffect, useState } from 'react';
import useRecordQuestion from '../hooks/useRecordQuestion';

const App: FC = () => {
	const [isMicro, setIsMicro] = useState(true);

	const [animNeznaika, setAnimNeznaika] = useState('i_do_not_no_hello');
	const [durationAudio, setDurationAudio] = useState(0);

	const [viewResponce, setViewResponce] = useState(false);

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

	const handleMicroClickStop = async () => {
		if (!isMicro) {
			await stopRecording();
			await receiveAudioStream();
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

	return (
		<div className='wrapper__app'>
			{!viewResponce ? (
				<img className='app__hello' src='./images/hello.png' alt='hello' />
			) : (
				<p className='text_answer'>
					Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat
					asperiores neque quod ad nam rem perferendis eaque quo molestias
					mollitia ducimus ex, modi unde labore explicabo, laboriosam magnam
					numquam ipsum? Lorem ipsum dolor sit, amet consectetur adipisicing
					elit. Dignissimos ipsam quam accusamus adipisci, veniam deserunt,
					autem eum nemo at vitae maiores. Ut magnam modi iste esse, voluptatem
					error quis possimus! Lorem ipsum dolor sit amet consectetur
					adipisicing elit.
				</p>
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