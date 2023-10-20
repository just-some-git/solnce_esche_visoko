# pip install os
# pip install torch

import os
import torch

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'

if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                   local_file)  

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

example_text = 'Ну, мой дорогой товарищ, небо голубое, потому что... как это было? Ах да, из-за чудо-явления, которое называется рассеянием света! Смешивается тут солнечный свет со всеми цветами радуги, и каждый цветик с разной длиной волны. А вот в атмосфере нашей земли частицы воздуха вот так крошечно-мелко разбрасывают этот свет во все стороны.'
sample_rate = 48000
speaker='baya'

audio_paths = model.save_wav(text=example_text,
                             speaker=speaker,
                             sample_rate=sample_rate)