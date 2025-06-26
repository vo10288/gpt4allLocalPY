import os
import json
import xml.etree.ElementTree as ET

def convert_log_to_txt(src_path, dst_path):
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as infile:
        content = infile.read()
    with open(dst_path, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(elem, str(key))
        if isinstance(val, dict):
            child.append(dict_to_xml('item', val))
        elif isinstance(val, list):
            for sub in val:
                child.append(dict_to_xml('item', sub if isinstance(sub, dict) else {'value': sub}))
        else:
            child.text = str(val)
    return elem

def convert_json_to_xml(src_path, dst_path):
    try:
        with open(src_path, 'r', encoding='utf-8', errors='ignore') as infile:
            data = json.load(infile)
        root = dict_to_xml('root', data)
        tree = ET.ElementTree(root)
        tree.write(dst_path, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        print(f"[Errore JSON -> XML] {src_path}: {e}")

def convert_files_in_directory(base_dir, output_base):
    for root_dir, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root_dir, file)
            rel_path = os.path.relpath(root_dir, base_dir)
            output_dir = os.path.join(output_base, rel_path)
            os.makedirs(output_dir, exist_ok=True)

            if file.endswith('.log'):
                new_filename = file[:-4] + '.txt'
                dst_path = os.path.join(output_dir, new_filename)
                print(f"[LOG -> TXT] {file_path} -> {dst_path}")
                convert_log_to_txt(file_path, dst_path)

            elif file.endswith('.json'):
                new_filename = file[:-5] + '.xml'
                dst_path = os.path.join(output_dir, new_filename)
                print(f"[JSON -> XML] {file_path} -> {dst_path}")
                convert_json_to_xml(file_path, dst_path)

if __name__ == "__main__":
    directory = input("📂 Inserisci il percorso della directory da convertire: ").strip()
    output_directory = os.path.join("log-converted")
    
    if os.path.isdir(directory):
        convert_files_in_directory(directory, output_directory)
        print(f"\n✅ Conversione completata. File salvati in: {output_directory}")
    else:
        print("❌ Directory non valida.")
