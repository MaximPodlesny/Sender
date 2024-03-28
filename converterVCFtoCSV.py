import csv
import quopri

def convert_vcf_to_csv(vcf_file, csv_file):
    

    with open(vcf_file, 'r', encoding='utf-8') as vcf_ob, open(csv_file, 'w', encoding='utf-8', newline='') as csv_ob:
        vcf_reader = list(csv.reader(vcf_ob, delimiter=':'))
        csv_writer = csv.DictWriter(csv_ob, fieldnames=['name', 'phone', 'org', 'email'])

        list_contacts = []
        d_row = {}
        counter = 1
        for i, row in enumerate(vcf_reader):
            if counter != 1:
                counter -= 1
                continue
            elif len(row) != 0 and 'END' not in row[0]:
                if 'FN' in row[0]:
                    d_row['name'] = row[-1]
                    
                    while i != (len(vcf_reader)-counter) and len(vcf_reader[i+counter]) != 0 and vcf_reader[i+counter][0].startswith('='):
                        d_row['name'] = f"{d_row.get('name', b'')}{vcf_reader[i+counter][0][1:]}"
                        counter += 1
                if 'ORG' in row[0]:
                    d_row['org'] = row[-1]
                    
                    while i != (len(vcf_reader)-counter) and len(vcf_reader[i+counter]) != 0 and vcf_reader[i+counter][0].startswith('='):
                        d_row['org'] = f"{d_row.get('org', b'')}{vcf_reader[i+counter][0][1:]}"
                        counter += 1
                elif 'TEL' in row[0]:
                    d_row['phone'] = '{} {}'.format(d_row.get('phone', ''), quopri.decodestring(row[-1]).decode('utf-8', 'ignor'))
                elif 'EMAIL' in row[0]:
                    d_row['email'] = d_row.get('email', '')
                
            elif len(row) != 0 and 'END' in row[0]:
                list_contacts.append(d_row)
                d_row = {}
        for d in list_contacts:
            d['name'] = quopri.decodestring(d.get('name', b'')).decode('utf-8', 'ignor')
            d['email'] = quopri.decodestring(d.get('email', b'')).decode('utf-8', 'ignor')
            d['org'] = quopri.decodestring(d.get('org', b'')).decode('utf-8', 'ignor')
        
        csv_writer.writeheader()
        csv_writer.writerows(list_contacts)
        print(f'В файле {len(list_contacts)} контактов.')