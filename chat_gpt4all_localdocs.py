import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import GPT4All
from langchain.chains import RetrievalQA

def log_message(file, role, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"[{timestamp}] {role.upper()}:\n{message}\n\n")
    file.flush()

def load_documents_from_extensions(folder, valid_exts):
    documents = []
    for ext in valid_exts:
        for file in Path(folder).rglob(f"*{ext}"):
            try:
                documents.append(TextLoader(str(file)).load()[0])
            except Exception as e:
                print(f"⚠️ Errore nel file {file}: {e}")
    return documents

def main():
    parser = argparse.ArgumentParser(description="Chat con GPT4All su documenti locali con estensioni multiple.")
    parser.add_argument("--model_path", required=True, help="Percorso del modello .gguf")
    parser.add_argument("--model_type", required=True, choices=["llama", "gptj", "mpt", "falcon"], help="Tipo di modello")
    parser.add_argument("--docs_dir", required=True, help="Cartella con i documenti")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"chatlog_{timestamp}.txt"
    log_file = open(log_filename, "w", encoding="utf-8")

    valid_exts = [".txt", ".md", ".log", ".csv", ".json"]
    print(f"\n📚 Caricamento documenti da: {args.docs_dir} con estensioni: {', '.join(valid_exts)}")

    documents = load_documents_from_extensions(args.docs_dir, valid_exts)
    if not documents:
        print("❌ Nessun documento valido trovato. Controlla la cartella.")
        return

    embeddings = GPT4AllEmbeddings()
    vectordb = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")

    llm = GPT4All(
        model=args.model_path,
        model_type=args.model_type,
        allow_download=False,
        n_threads=os.cpu_count() or 4,
        backend="llama"
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )

    print("\n✅ Chat pronta. Fai domande sui documenti. Premi CTRL+C per uscire.\n")

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
        print("\n🛑 Chat terminata. Log salvato in:", log_filename)
        log_file.close()

if __name__ == "__main__":
    main()
