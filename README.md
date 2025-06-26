# gpt4allLocalPY

wget https://huggingface.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF/blob/main/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf

python3 chat_gpt4all_localdocs.py \
  --model_path /modelli/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf \
  --docs_dir /percorso/documenti_normalized



#PYTHON PIP INSTALL:

pip install -r requirements.txt

APT INSTALL:

sudo apt update
xargs -a requirements_install_apt.txt sudo apt install -y

OR:

cat requirements_install_apt.txt | xargs sudo apt install -y


# PYTHON 3.9 OR PYTHON 3.10

# 🧹 Document Normalizer for GPT4All

This project allows you to **normalize documents** of various formats (PDF, DOCX, DOC, ODT, HTML...) into plain `.txt` files suitable for analysis by **GPT4All** (offline large language model).

It includes:
- A Bash script for converting and normalizing documents
- A Python script to embed documents and ask questions using a local GPT4All `.gguf` model

---

## 📦 Supported Input Formats

| Format      | Tool Used         |
|-------------|-------------------|
| `.pdf`      | `pdftotext`       |
| `.docx`     | `docx2txt`        |
| `.doc`      | `antiword`        |
| `.odt`      | `odt2txt`         |
| `.html`     | `html2text`       |
| `.htm`      | `html2text`       |

---

## 🚀 Quick Start

### 1. Run the Bash Normalizer

```bash
chmod +x normalize_folder.sh
./normalize_folder.sh /path/to/your/documents

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

OR

conda create -n gpt4all-env python=3.10
conda activate gpt4all-env
pip install -r requirements.txt

AFTER

python3 chat_gpt4all_multifile.py \
  --model_path /path/to/model/mistral-7b-instruct.Q4_0.gguf \
  --model_type llama \
  --docs_dir /path/to/your/documents_normalized

Folder Structure Example

Input:

/documents/
  ├── file1.docx
  └── subfolder/
      └── notes.pdf

Output:

/documents_normalized/
  ├── file1.txt
  └── subfolder/
      └── notes.txt

Dependencies (automatically installed)

The following tools will be checked and installed by the script if missing:

    poppler-utils (for pdftotext)

    docx2txt

    antiword

    odt2txt

    html2text

🔐 GPT4All Model Note

Make sure you download your .gguf model from https://gpt4all.io/models or HuggingFace and provide the full path via --model_path.
🧑‍💻 Author

Developed by Antonio 'Visi@n' Broi
antonio@tsurugi-linux.org
https://tsurugi-linux.org

 NVIDIA CUDA TOOLKIT
sudo apt install nvidia-cuda-toolkit
nvidia-smi
sudo apt install libcudart11.0
apt search libcudart



langchain>=0.2.0
langchain-community>=0.0.22
gpt4all>=2.4
chromadb


License: MIT




