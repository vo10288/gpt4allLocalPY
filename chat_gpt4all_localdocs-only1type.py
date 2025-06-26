import os
import sys
import argparse
from datetime import datetime
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import GPT4All
from langchain.chains import RetrievalQA

def log_message(file, role, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"[{timestamp}] {role.upper()}:\n{message}\n\n")
    file.flush()

def main():
    parser = argparse.ArgumentParser(description="Chat con GPT4All su documenti locali.")
    parser.add_argument("--model_path", required=True, help="Percorso del modello .gguf")
    parser.add_argument("--model_type", required=True, choices=["llama", "gptj", "mpt", "falcon"], help="Tipo di modello")
    parser.add_argument("--docs_dir", required=True, help="Cartella con i documenti")
    parser.add_argument("--ext", default=".txt", help="Estensione file da analizzare (default: .txt)")
    args = parser.parse_args()

    # Log file con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"chatlog_{timestamp}.txt"
    log_file = open(log_filename, "w", encoding="utf-8")

    print(f"\n📚 Indicizzazione dei documenti da: {args.docs_dir} (estensione: {args.ext})")

    loader = DirectoryLoader(args.docs_dir, glob=f"**/*{args.ext}", loader_cls=TextLoader)
    documents = loader.load()
    embeddings = GPT4AllEmbeddings()
    vectordb = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")

    # Inizializza LLM GPT4All
    llm = GPT4All(
        model=args.model_path,
        model_type=args.model_type,
        allow_download=False,
        n_threads=os.cpu_count() or 4,
        backend='llama'
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )

    print("✅ Pronto. Fai domande sui documenti. CTRL+C per uscire.\n")

    try:
        while True:
            question = input("👤 Tu: ").strip()
            if not question:
                continue
            log_message(log_file, "utente", question)
            response = qa_chain.run(question)
            print(f"🤖 GPT4All: {response}")
            log_message(log_file, "gpt4all", response)
    except KeyboardInterrupt:
        print("\n🛑 Uscita richiesta. Log salvato in:", log_filename)
        log_file.close()

if __name__ == "__main__":
    main()
