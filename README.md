### Parser de fichier de logs VMWare ESXI ###
###          12/01/25                     ###

Description : script qui parse un fichier de logs VMWare ESXI et extrait les champs au format json

# Prérequis

- Travailler sur un système Linux

- Pour le parser : python3
Pour l'installer : 
$ sudo apt install python3 

- Pour les tests : p
Pour l'installer sur un environnement virtuel :
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install pytest

# Lancement de parser

Pour lancer le script :
$ python3 log_file_parser.py -f <input_file>

Sortie : Fichier JSON input_file_name.json contenant les informations suivantes : 
{Protocole, Received, Send, Local IP Address, Local Port, Remote Adress, Remote Port, State, World ID, CC algo, World Name}


# Tests unitaires

Avant de lancer le script, modifier dans le code le filepath des fichiers input_file et output_file (lignes 7 et 8):
input_file = "/home/user/esxcli_network_ip_connection_list.txt"
output_file = "/home/user/esxcli_network_ip_connection_list"

Pour lancer les tests :
$ pytest test_log_file_parser.py


