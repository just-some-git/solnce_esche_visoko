from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import numpy as np

np.random.seed(42)
torch.manual_seed(42)

def load_tokenizer_and_model(model_name):
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    return tokenizer, model

def generate(
    model, tok, text,
    do_sample=True, max_length=50, repetition_penalty=5.0,
    top_k=5, top_p=0.95, temperature=1,
    num_beams=None,
    no_repeat_ngram_size=3
    ):
  input_ids = tok.encode(text, return_tensors="pt")
  
  # Create an attention mask with all values set to 1
  attention_mask = torch.ones(input_ids.shape, dtype=input_ids.dtype)

  # Generate text with the provided settings
  out = model.generate(
      input_ids,
      attention_mask=attention_mask,  # Include the attention mask
      max_length=max_length,
      repetition_penalty=repetition_penalty,
      do_sample=do_sample,
      top_k=top_k, top_p=top_p, temperature=temperature,
      num_beams=num_beams,
      no_repeat_ngram_size=no_repeat_ngram_size,
      pad_token_id=tok.eos_token_id  # Set pad_token_id to eos_token_id
      )
  return list(map(tok.decode, out))

# Example context and question
question = "Почему небо голубое?"
text_with_context = question  # Combine context and question

tok, model = load_tokenizer_and_model("ai-forever/rugpt3large_based_on_gpt2")
generated = generate(model, tok, text_with_context, num_beams=10)
for text in generated:
    print(text)