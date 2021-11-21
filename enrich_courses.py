import csv
import json

event_id = 277
target_encoding = "iso-8859-1"
mapping_file = f'mapping_{event_id}.json'
files = {f'hajontakanta_{event_id}.txt': 1,
         f'kilpailijat_{event_id}.txt': 2,
         f'radat_{event_id}.txt': 2,
         f'sarjat_{event_id}.txt': 1
         }


def read_mappings(filename):
    f = open(filename, )
    data = json.load(f)
    f.close()
    return data


def read_file(filename):
    data = []
    with open(filename, newline='', encoding='iso-8859-1') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f,
                            delimiter='|',
                            quoting=csv.QUOTE_NONE,
                            dialect=dialect)
        for row in reader:
            data.append(row)

    return data


def map_classes(rows, class_mappings, field):
    result = []
    for row in rows:
        if not row[field] in class_mappings:
            raise BaseException(f'Fehler: Klassenzuordnung für {row[field]} '
                                f'fehlt!')
            # result.append(row)
            # continue

        addon = ''
        for class_name in class_mappings[row[field]]:
            if len(addon) > 0:
                addon += ', '

            addon += class_name

        new_row = row
        new_row[field] += ': ' + addon
        result.append(new_row)

    return result


def write_file(filename, rows):
    with open("patched/" + filename, 'w', newline='',
              encoding=target_encoding) as f:
        writer = csv.writer(f, delimiter='|', quoting=csv.QUOTE_NONE)
        writer.writerows(rows)


mappings = read_mappings(mapping_file)

for key in files.keys():
    content = read_file(key)
    mapped_rows = map_classes(content, mappings, files[key])
    write_file(key, mapped_rows)
