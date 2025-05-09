import streamlit as st
import torch
import json
import re

# --- Load Tokenizer from JSON ---
class CustomTokenizer:
    def __init__(self):
        with open("tokenizer.json", "r") as f:
            tokenizer_dict = json.load(f)
        self.word2idx = tokenizer_dict["word2idx"]
        self.idx2word = {int(k): v for k, v in tokenizer_dict["idx2word"].items()}
        self.vocab_size = tokenizer_dict["vocab_size"]
        self.special_tokens = tokenizer_dict["special_tokens"]

    def tokenize(self, text):
        return re.findall(r'\w+|[^\w\s]', text.lower())

    def encode(self, text):
        tokens = self.tokenize(text)
        return [self.word2idx.get(token, self.word2idx["<pad>"]) for token in tokens]

    def decode(self, token_ids):
        tokens = [self.idx2word.get(idx, "<unk>") for idx in token_ids]
        return " ".join(tokens)

# Load the tokenizer
tokenizer = CustomTokenizer()

# Define special token IDs
SOS_TOKEN_ID = tokenizer.word2idx["<sos>"]
EOS_TOKEN_ID = tokenizer.word2idx["<eos>"]
PAD_TOKEN_ID = tokenizer.word2idx["<pad>"]

# --- Load the Model ---
class PositionalEncoding(torch.nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(torch.log(torch.tensor(10000.0)) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :].to(x.device)

class Transformer(torch.nn.Module):
    def __init__(self, num_layers, d_model, num_heads, dff, vocab_size):
        super().__init__()
        self.embedding = torch.nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model)
        self.transformer = torch.nn.Transformer(
            d_model=d_model,
            nhead=num_heads,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            dim_feedforward=dff,
            batch_first=True
        )
        self.fc_out = torch.nn.Linear(d_model, vocab_size)

    def forward(self, src, tgt):
        src_emb = self.pos_encoding(self.embedding(src))
        tgt_emb = self.pos_encoding(self.embedding(tgt))
        src_padding_mask = (src == PAD_TOKEN_ID)
        tgt_padding_mask = (tgt == PAD_TOKEN_ID)
        tgt_mask = torch.nn.Transformer.generate_square_subsequent_mask(tgt.size(1)).to(tgt.device)
        out = self.transformer(
            src_emb, tgt_emb,
            src_key_padding_mask=src_padding_mask,
            tgt_key_padding_mask=tgt_padding_mask,
            tgt_mask=tgt_mask
        )
        return self.fc_out(out)

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Transformer(
    num_layers=4,
    d_model=256,
    num_heads=4,
    dff=1024,
    vocab_size=tokenizer.vocab_size
).to(device)
model.load_state_dict(torch.load("transformer_model.pth", map_location=device))
model.eval()

# --- Code-to-Pseudocode Generation Function ---
def generate_pseudocode(model, cpp_code, max_len=100):
    model.eval()
    with torch.no_grad():
        # Split C++ code into individual lines
        cpp_lines = cpp_code.strip().split('\n')
        generated_pseudo_lines = []

        for line in cpp_lines:
            # Tokenize the current line of C++ code
            src_tokens = [SOS_TOKEN_ID] + tokenizer.encode(line) + [EOS_TOKEN_ID]
            src = torch.tensor([src_tokens]).to(device)
            tgt = torch.tensor([[SOS_TOKEN_ID]]).to(device)

            # Generate pseudocode for the current line
            for _ in range(max_len):
                output = model(src, tgt)
                next_token = output[:, -1, :].argmax(dim=-1).item()
                if next_token == EOS_TOKEN_ID:
                    break
                tgt = torch.cat([tgt, torch.tensor([[next_token]]).to(device)], dim=1)

            # Decode the generated tokens and remove <sos> and <eos>
            decoded_tokens = tokenizer.decode(tgt[0].tolist())
            decoded_tokens = decoded_tokens.replace("<sos>", "").replace("<eos>", "").strip()
            generated_pseudo_lines.append(decoded_tokens)

        # Join all generated lines into a single string
        return "\n".join(generated_pseudo_lines)

# --- Streamlit App ---
st.title("C++ Code to Pseudocode Generator")

# Input text area for C++ code
cpp_code = st.text_area("Enter your C++ code here:", height=200)

# Generate button
if st.button("Generate Pseudocode"):
    if cpp_code.strip():
        # Generate pseudocode
        generated_pseudo = generate_pseudocode(model, cpp_code)
        st.subheader("Generated Pseudocode:")
        st.text(generated_pseudo)
    else:
        st.warning("Please enter some C++ code.")