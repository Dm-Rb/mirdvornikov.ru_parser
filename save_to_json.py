import os
import json

def save(content_item):
    print(f'saving -> {content_item["name"]}')
    SAVEFOLDER = 'D:\\mirdvornikov'
    structure = {
        "version": "td",
        "items": []
    }
    if not os.path.isdir(SAVEFOLDER):
        os.mkdir(SAVEFOLDER)
    files = os.listdir(SAVEFOLDER)
    files = list(filter(lambda x: x.endswith('.json'), files))
    # if there are no files in the folder -> create first file
    if not files:

        structure["items"].append(content_item)
        with open(os.path.join(SAVEFOLDER, '1.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(structure, ensure_ascii=False, indent=2))
    else:
        # get file with a large number_name
        files = sorted(files, key=lambda x: int(x.replace('.json', '')), reverse=True)
        current_file = files[0]
        if os.path.getsize(os.path.join(SAVEFOLDER, current_file)) <= 104857600:
            with open(os.path.join(SAVEFOLDER, current_file), 'r', encoding='utf-8') as f:
                data_f = json.load(f)
                data_f["items"].append(content_item)
            with open(os.path.join(SAVEFOLDER, current_file), 'w', encoding='utf-8') as f:
                json.dump(data_f, f, ensure_ascii=False, indent=2)
        else:
            current_file = str(int(current_file.replace('.json', '')) + 1) + '.json'

            structure["items"].append(content_item)
            with open(os.path.join(SAVEFOLDER, current_file), 'w', encoding='utf-8') as f:
                f.write(json.dumps(structure, ensure_ascii=False, indent=2))









