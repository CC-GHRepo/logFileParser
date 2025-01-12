import argparse
import json
import os

def parse_file(input_file):
    try:

        input_file_name = input_file.split('.')[0]
        output_file = input_file_name + ".json"

        with open(input_file, "r", encoding='utf-8') as in_file:

            lines = in_file.readlines()

            if(len(lines) == 0):
                print(f"Le fichier {input_file} est vide.")
                return

            # Taille des colonnes (défini par les "-" sur la 2ème ligne du fichier)
            col_len = [len(col) for col in lines[1].split()]

            json_field_names = [
                "Protocole", 
                "Received", 
                "Send", 
                "Local IP Address", 
                "Local Port", 
                "Remote Address", 
                "Remote Port", 
                "State", 
                "World ID", 
                "CC algo", 
                "World Name"
            ]

            # On remplit le json avec les champs correspondants à partir de la 3ème ligne
            with open(output_file, "w", encoding='utf-8') as out_file:
                
                out_file.write("[\n")
                first_line = True

                for line in lines[2:]:
                    
                    json_line = {}
                    offset = 0
                    j = 0

                    for i in range(len(col_len)):

                        length = col_len[i]
                        json_value = line[offset:offset+length].strip()

                        if j < len(json_field_names):
        
                            if i == 3 or i == 4:                
                                # Gestion des cas particuliers pour les champs Local Address et Foreign Address 
                                # du fichier de logs qui contiennent l'adresse et le port dans le même champ
                                address = json_value.split(':')[0]
                                json_line[json_field_names[j]] = address
                                port = ''
                                if(len(json_value.split(':')) > 1):
                                    port = json_value.split(':')[1]
                                json_line[json_field_names[j+1]] = port
                                j += 2
                            else:
                                json_line[json_field_names[j]] = json_value
                                j += 1
                        offset += length + 2
                        
                    if first_line:
                        json.dump(json_line, out_file)
                        first_line = False
                    else:
                        out_file.write(",\n")
                        json.dump(json_line, out_file)

                out_file.write("\n]")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser de fichier de logs VMWare ESXi")
    parser.add_argument('-f', '--file', type=str, required=True, help="Fichier de logs à parser")

    args = parser.parse_args()

    input_file = args.file

    if not os.path.exists(input_file):
        print(f"Le fichier {input_file} n'existe pas.")
    elif not input_file.endswith(".txt"):
        print("Le fichier de logs doit être au format .txt.")
    else:
        parse_file(input_file)
