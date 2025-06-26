#!/bin/bash

set -e

# Verifica input
if [ -z "$1" ]; then
    echo "❌ Usa: $0 /percorso/cartella_input"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="${INPUT_DIR%/}_normalized"

# Tool richiesti
declare -A tools=(
  [pdftotext]=poppler-utils
  [docx2txt]=docx2txt
  [antiword]=antiword
  [odt2txt]=odt2txt
  [html2text]=html2text
)

echo "🔍 Controllo tool richiesti..."
for tool in "${!tools[@]}"; do
  if ! command -v "$tool" &> /dev/null; then
    echo "⚠️  Tool $tool non trovato. Installo con: sudo apt-get install ${tools[$tool]}"
    sudo apt-get update
    sudo apt-get install -y "${tools[$tool]}"
  else
    echo "✅ $tool è disponibile."
  fi
done

echo "📂 Cartella di input: $INPUT_DIR"
echo "📁 Cartella di output: $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

echo "🚀 Avvio normalizzazione..."

# Loop su tutti i file supportati
find "$INPUT_DIR" -type f \( -iname "*.pdf" -o -iname "*.docx" -o -iname "*.doc" -o -iname "*.odt" -o -iname "*.html" -o -iname "*.htm" \) | while read -r file; do
    rel_path="${file#$INPUT_DIR/}"
    rel_dir=$(dirname "$rel_path")
    filename=$(basename "$file")
    name="${filename%.*}"
    ext="${filename##*.}"
    ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    output_subdir="$OUTPUT_DIR/$rel_dir"
    mkdir -p "$output_subdir"
    output_file="$output_subdir/$name.txt"

    case "$ext_lower" in
        pdf)
            pdftotext "$file" "$output_file"
            ;;
        docx)
            docx2txt "$file" "$output_file"
            ;;
        doc)
            antiword "$file" > "$output_file"
            ;;
        odt)
            odt2txt "$file" > "$output_file"
            ;;
        html|htm)
            html2text "$file" > "$output_file"
            ;;
        *)
            echo "❌ Formato non supportato: $file"
            continue
            ;;
    esac
    echo "✅ Convertito: $file → $output_file"
done

echo "🏁 Normalizzazione completata. File convertiti in: $OUTPUT_DIR"
