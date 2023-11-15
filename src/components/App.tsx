import { FC, useEffect, useState } from 'react';
import useActualeDate from '../hooks/useActualDate';
import useRecordQuestion from '../hooks/useRecordQuestion';

const App: FC = () => {
	const [isMicro, setIsMicro] = useState<boolean>(true);

	const [animNeznaika, setAnimNeznaika] = useState<string>(
		'i_do_not_know_hello'
	);
	const [durationAudio, setDurationAudio] = useState<number>(0);
	const [textRequest, setTextRequest] = useState<string>('');

	const [isWaitAnswer, setIsWaitAnswer] = useState<boolean>(false);

	// let text = '';
	const [text, setText] = useState();
	const [test, setTest] = useState(false);

	let nameAudio;

	const { actualDate } = useActualeDate();

	const [viewResponce, setViewResponce] = useState<boolean>(false);

	const { startReq, recognition, stopReq } = useRecordQuestion();
	// const {
	// 	receiveAudioStream,
	// 	receivedAudioUrl,
	// 	addText,
	// 	text,
	// 	setText,
	// 	test,
	// 	setTest,
	// 	textRequest,
	// 	durationAudio,
	// } = useRequestQuestion();

	useEffect(() => {
		console.log('use:', text);
	}, [text]);

	useEffect(() => {
		// когда время длительности аудио проходит, убирает текст ответа. А другой юз эффект меняет анимацию
		let stopAnim = setTimeout(() => {
			setViewResponce(false);
		}, durationAudio);
		return () => {
			clearTimeout(stopAnim);
		};
	}, [durationAudio]);

	let receivedAudioUrl;

	const playAudio = audioUrl => {
		const audio = new Audio(audioUrl);
		audio.play();
		setViewResponce(true);
		setAnimNeznaika('i_do_not_know');
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
				`http://127.0.0.1:8000/answers/${nameAudio}/`
			);
			const data = await responce.json();
			const text = data.text;
			setTextRequest(text);
		} catch (error) {
			console.log(error);
		}
	};

	const handleMicroClickPlay = () => {
		if (isMicro) {
			startReq();
			console.log('play');
			setIsMicro(false);
		}
	};

	useEffect(() => {
		//HELP: ОСНОВНОЙ ВАРИАНТ АНИМАЦИИ
		// когда исчезает текст ответа, меняет анимацию на начальную
		if (!viewResponce) {
			setAnimNeznaika('i_do_not_know_hello');
		} else {
			// if (textRequest === 'булка') {
			// 	let anim = setTimeout(() => {
			// 		setAnimNeznaika('i_do_not_know_wait');
			// 		console.log('poluchilos');
			// 	}, durationAudio - 3000);

			// 	return () => {
			// 		clearTimeout(anim);
			// 	};
			// } else if (textRequest === 'пусто') {
			// 	let anim = setTimeout(() => {
			// 		setAnimNeznaika('negative_response');
			// 		console.log('poluchilos');
			// 	}, durationAudio - 3000);

			// 	return () => {
			// 		clearTimeout(anim);
			// 	};

			if (durationAudio <= 6000) {
				let anim = setTimeout(() => {
					setAnimNeznaika('i_do_not_know_wait');
				}, durationAudio - 3000);

				return () => {
					clearTimeout(anim);
				};
			} else {
				let wait = setTimeout(() => {
					setIsWaitAnswer(true);
				}, 3000);

				let anim = setTimeout(() => {
					setIsWaitAnswer(false);
					setAnimNeznaika('i_do_not_know_wait');
				}, durationAudio - 3000);

				return () => {
					clearTimeout(anim);
					clearTimeout(wait);
				};
			}
		}
	}, [viewResponce]);

	// useEffect(() => { //HELP: ЗАПАСНОЙ ВАРИАНТ АНИМАЦИИ
	// 	if (!viewResponce) {
	// 		setAnimNeznaika('i_do_not_know_hello');
	// 	} else {
	// 		let anim = setTimeout(() => {
	// 			setAnimNeznaika('i_do_not_know_wait');
	// 		}, durationAudio - 3000);

	// 		return () => {
	// 			clearTimeout(anim);
	// 		};
	// 	}
	// }, [viewResponce]);

	recognition.onresult = async function (event) {
		const transcript = event.results[0][0].transcript;
		//Если делать черезе переменную test a не useState// text = transcript;
		setText(transcript);
		if (event.results[0].isFinal) {
			setIsMicro(true);
		}
		//Если делать черезе переменную test a не useState // await receiveAudioStream();
		// await addText();
		// await playAudio(receivedAudioUrl);
		setTest(true);
	};

	useEffect(() => {
		const fetchData = async () => {
			await receiveAudioStream();
			await addText();
			await playAudio(receivedAudioUrl);
		};

		if (test) {
			fetchData();
			setTest(false);
		}
	}, [test]);
	//////////////////
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		//таблетка от бликов
		const animLoading = setTimeout(() => {
			setIsLoading(false);
		}, 13000);

		return () => {
			clearTimeout(animLoading);
		};
	}, []);
	const arrAnimation = [
		'i_do_not_know',
		'i_do_not_know_wait',
		'i_do_not_know_hello',
		'negative_response',
		'micro',
		'bg_main',
	];
	//////////////////////////

	return (
		<>
			{isLoading ? (
				<div className='wrapper__loading'>
					{arrAnimation.map(anim => {
						return (
							<div
								key={anim}
								className='test'
								style={{ animation: `${anim} 3s linear infinite` }}
							></div>
						);
					})}

					<svg
						className='svg-animation'
						width='100'
						height='100'
						xmlns='http://www.w3.org/2000/svg'
					>
						<circle
							cx='50'
							cy='50'
							r='40'
							stroke='#3498db'
							strokeWidth='4'
							fill='none'
						>
							<animate
								attributeName='stroke-dashoffset'
								dur='2s'
								from='0'
								to='502'
								repeatCount='indefinite'
							/>
							<animate
								attributeName='stroke-dasharray'
								dur='2s'
								values='150.79644737231007 100.53096491487338;1 250;150.79644737231007 100.53096491487338'
								repeatCount='indefinite'
							/>
						</circle>
					</svg>
				</div>
			) : (
				<div className='wrapper__app'>
					{!viewResponce ? (
						<img className='app__hello' src='./images/hello.png' alt='hello' />
					) : (
						<p className='text_answer'>{textRequest}</p>
					)}
					{isWaitAnswer ? (
						<div className='animation_wait'></div>
					) : (
						<div
							className='animation'
							style={{ animation: `${animNeznaika} 3s linear infinite` }}
						></div>
					)}

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
			)}
		</>
	);
};

export default App;
