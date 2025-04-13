# 🌟 C++ Code to Pseudocode Generator | Transformer from Scratch

This project features a **Transformer-based Sequence-to-Sequence (Seq2Seq) model** that translates **C++ code ➝ pseudocode**. Built entirely from scratch in **PyTorch**, this project does not use pretrained models and provides an in-depth educational example of a Transformer model.

The model has been deployed with an interactive **Streamlit** web app, allowing users to generate pseudocode from C++ code easily.

---

## 📌 Key Features

- 🔹 **Transformer-based Model**: Built from scratch using `torch.nn.Transformer` for C++ to pseudocode translation.
- 🔹 **Custom Tokenizer**: Handles tokenization of C++ code and pseudocode with special tokens like `<sos>`, `<eos>`, and `<pad>`.
- 🔹 **Interactive Streamlit Web App**: Allows users to input C++ code and generate corresponding pseudocode in real time.
- 🔹 **Cleaned Dataset**: Trained on a customized SPOC dataset, preprocessed to handle missing or misaligned pseudocode entries.

---

## 🚀 Demo

Try it out yourself:

🔗 **Live Streamlit App**: *[Streamlit link here](https://xc2vptrxpbfryq3axfuuax.streamlit.app/)*  
🔗 **Medium Blog**: *[Medium blog link here](https://medium.com/@sami68/turning-code-into-logic-building-a-c-to-pseudocode-transformer-from-scratch-0c8505179f90)*  

---

## 🧠 Concepts Used

### ✨ Transformer (Seq2Seq) – From Scratch
- Encoder-Decoder architecture using `torch.nn.Transformer`
- **Positional Encoding** to retain sequence order
- **Multi-head attention** and **feed-forward layers** for processing complex code relationships
- **Greedy decoding loop** for generating output

### ✨ Tokenization
- Custom word-level tokenizer
- Special tokens handling: `<sos>`, `<eos>`, `<pad>`, `<unk>`
  
### ✨ Dataset
- **SPOC Dataset**: A curated dataset containing C++ code and corresponding pseudocode pairs.
- **Preprocessing**: Missing or misaligned pseudocode and code were realigned to ensure the quality of training data.

---

## 🧪 Model Architecture
    [C++ Code] 
       ↓ 
    Tokenization + <sos>/<eos> 
       ↓
    Embedding + Positional Encoding
       ↓
    Transformer Encoder-Decoder
       ↓
    Linear Layer + Softmax 
       ↓
    [Generated Pseudocode]
## Sample Outputs:
   ![image](https://github.com/user-attachments/assets/e7107994-188e-4d69-8364-1964eeb94f2a)


