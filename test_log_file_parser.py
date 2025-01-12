import argparse
import os
import re
import pytest
import json

input_file = "/home/user/esxcli_network_ip_connection_list.txt"
output_file = "/home/user/esxcli_network_ip_connection_list"

# Vérification de l'existence du fichier en entrée
def test_input_file_exists(): 
    os.path.exists(input_file), f"Le fichier {input_file} n'existe pas."

# Vérification de l'entension du fichier en entrée (.txt)
def test_file_extension():    
    assert input_file.endswith(".txt"), "Le fichier n'est pas au bon format."

# Vérification que le fichier en entrée n'est pas vide
def test_empty_input_file():
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        assert len(lines) > 0, f"Le fichier {input_file} est vide."
    except FileNotFoundError:
        return

# Vérification que le fichier en entrée fait au moins 2 lignes (header)
def test_empty_input_file():
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        assert len(lines) > 2, f"Le fichier {input_file} est invalide."
    except FileNotFoundError:
        return

# Vérification qu'il s'agit bien d'un fichier de logs avec le bon header
def test_log_file_format():

    expected_header = [
        "Proto", 
        "Recv Q", 
        "Send Q", 
        "Local Address", 
        "Foreign Address", 
        "State", 
        "World ID", 
        "CC Algo", 
        "World Name"
    ]

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

            if not len(lines) > 2:
                return

            col_len = [len(col) for col in lines[1].split()]

            offset = 0
            header = []
            line = lines[0]
            for i in range(len(col_len)):
                length = col_len[i]
                header.append(line[offset:offset+length].strip())
                offset += length + 2

            assert header == expected_header, f"L'en-tête du fichier {input_file} est incorrect"

    except FileNotFoundError:
        return
      
# Vérification de l'existence du fichier en sortie
def test_output_file_exists(): 
    os.path.exists(output_file), f"Le fichier {output_file} n'existe pas."

# Véfification du format du fichier de sortie
def test_json_file_format():
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), "Le contenu du fichier json est incorrect."
    except json.JSONDecodeError:
        pytest.fail(f"Le fichier {output_file} n'est pas au formar json.")
    except FileNotFoundError:
        return

# Vérification que le fichier en sortie n'est pas vide
def test_empty_output_file():
    try:
        with open(output_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        assert len(lines) > 0, f"Le fichier {output_file} est vide."
    except FileNotFoundError:
        return
    
def test_json_field_values():
    try:    
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Test de la ligne 1
        # tcp         0       0  127.0.0.1:80     127.0.0.1:40033      ESTABLISHED   2098838  docker1  envoy
        test_1 = data[0]
        assert test_1["Protocole"] == "tcp", "Le champ 'Protocole' du test 1 est incorrect"
        assert test_1["Received"] == "0", "Le champ 'Received' du test 1 est incorrect"
        assert test_1["Send"] == "0", "Le champ 'Send' du test 1 est incorrect"
        assert test_1["Local IP Address"] == "127.0.0.1", "Le champ 'Local IP Address' du test 1 est incorrect"
        assert test_1["Local Port"] == "80", "Le champ 'Local Port' du test 1 est incorrect"
        assert test_1["Remote Address"] == "127.0.0.1", "Le champ 'Remote Address' du test 1 est incorrect"
        assert test_1["Remote Port"] == "40033", "Le champ 'Remote Port' du test 1 est incorrect"
        assert test_1["State"] == "ESTABLISHED", "Le champ 'State' du test 1 est incorrect"
        assert test_1["World ID"] == "2098838", "Le champ 'World ID' du test 1 est incorrect"
        assert test_1["CC algo"] == "docker1", "Le champ 'CC algo' du test 1 est incorrect"
        assert test_1["World Name"] == "envoy", "Le champ 'World Name' du test 1 est incorrect"
        
        # Test de la ligne 5
        # tcp         0       0  127.0.0.1:20923  127.0.0.1:80         TIME WAIT           0
        test_2 = data[4]
        assert test_2["Protocole"] == "tcp", "Le champ 'Protocole' du test 2  est incorrect"
        assert test_2["Received"] == "0", "Le champ 'Received' du test 2  est incorrect"
        assert test_2["Send"] == "0", "Le champ 'Send' du test 2  est incorrect"
        assert test_2["Local IP Address"] == "127.0.0.1", "Le champ 'Local IP Address' du test 2  est incorrect"
        assert test_2["Local Port"] == "20923", "Le champ 'Local Port' du test 2  est incorrect"
        assert test_2["Remote Address"] == "127.0.0.1", "Le champ 'Remote Address' du test 2  est incorrect"
        assert test_2["Remote Port"] == "80", "Le champ 'Remote Port' du test 2  est incorrect"
        assert test_2["State"] == "TIME WAIT", "Le champ 'State' du test 2  est incorrect"
        assert test_2["World ID"] == "0", "Le champ 'World ID' du test 2  est incorrect"
        assert test_2["CC algo"] == "", "Le champ 'CC algo' du test 2  est incorrect"
        assert test_2["World Name"] == "", "Le champ 'World Name' du test 2  est incorrect"
        
        # Test de la ligne 42
        # tcp         0       0  127.0.0.1:9131   0.0.0.0:0            LISTEN        2098968  newreno  hostd
        test_3 = data[41]
        assert test_3["Protocole"] == "tcp", "Le champ 'Protocole' du test 3 est incorrect"
        assert test_3["Received"] == "0", "Le champ 'Received' du test 3 est incorrect"
        assert test_3["Send"] == "0", "Le champ 'Send' du test 3 est incorrect"
        assert test_3["Local IP Address"] == "127.0.0.1", "Le champ 'Local IP Address' du test 3 est incorrect"
        assert test_3["Local Port"] == "9131", "Le champ 'Local Port' du test 3 est incorrect"
        assert test_3["Remote Address"] == "0.0.0.0", "Le champ 'Remote Address' du test 3 est incorrect"
        assert test_3["Remote Port"] == "0", "Le champ 'Remote Port' du test 3 est incorrect"
        assert test_3["State"] == "LISTEN", "Le champ 'State' du test 3 est incorrect"
        assert test_3["World ID"] == "2098968", "Le champ 'World ID' du test 3 est incorrect"
        assert test_3["CC algo"] == "newreno", "Le champ 'CC algo' du test 3 est incorrect"
        assert test_3["World Name"] == "hostd", "Le champ 'World Name' du test 3 est incorrect"
        
        # Test de la ligne 65
        # udp         0       0  127.0.0.1:10672  127.0.0.1:6831                     2098968           hostd
        test_4 = data[64]
        assert test_4["Protocole"] == "udp", "Le champ 'Protocole' du test 4  est incorrect"
        assert test_4["Received"] == "0", "Le champ 'Received' du test 4  est incorrect"
        assert test_4["Send"] == "0", "Le champ 'Send' du test 4  est incorrect"
        assert test_4["Local IP Address"] == "127.0.0.1", "Le champ 'Local IP Address' du test 4  est incorrect"
        assert test_4["Local Port"] == "10672", "Le champ 'Local Port' du test 4  est incorrect"
        assert test_4["Remote Address"] == "127.0.0.1", "Le champ 'Remote Address' du test 4  est incorrect"
        assert test_4["Remote Port"] == "6831", "Le champ 'Remote Port' du test 4  est incorrect"
        assert test_4["State"] == "", "Le champ 'State' du test 4  est incorrect"
        assert test_4["World ID"] == "2098968", "Le champ 'World ID' du test 4  est incorrect"
        assert test_4["CC algo"] == "", "Le champ 'CC algo' du test 4  est incorrect"
        assert test_4["World Name"] == "hostd", "Le champ 'World Name' du test 4  est incorrect"
        
    except FileNotFoundError:
        return

