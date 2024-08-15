#!/usr/bin/env python3

import sys
import subprocess
from getuserclass import jsonify_pjsip, get_class_mapping, get_user_class


def line_is_context(l):
    l = l.strip()
    if len(l) < 3:
        return (False, '')
    if l[0] == '[' and l[1] != ']':
        ctxt = l[1:].split(']')[0]
        return (True, ctxt)
    return (False, '')

def get_class_passwords(config_file):
    class_passwords = {}
    current_class = None

    try:
        with open(config_file, 'r') as f:
            for line in f:
                is_context, context_name = line_is_context(line)
                if is_context:
                    current_class = context_name
                elif "password" in line and current_class and current_class.endswith("_class_auth"):
                    password = line.split('=')[1].strip()
                    class_name = current_class.split("_")[0]
                    class_passwords[class_name] = password
    except FileNotFoundError:
        sys.stderr.write(f"Erreur: Le fichier {config_file} est introuvable.\n")
    except Exception as e:
        sys.stderr.write(f"Erreur: {str(e)}\n")

    return class_passwords

def set_variable(name, value):
    command = f"perl /var/lib/asterisk/agi-bin/save_var.pl {name} {value}"
    subprocess.run(command, shell=True)


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        sys.stderr.write("Erreur: Ce script nécessite deux arguments.\n")
        return

    callerid_num = args[0]
    password_entered = args[1]
    print(f"CallerID: {callerid_num}, Password entered: {password_entered}")

    config_file = "/etc/asterisk/pjsip.conf"
    class_passwords = get_class_passwords(config_file)
    class_name = identify_class(callerid_num)
    
    if class_name and class_name in class_passwords:
        password = class_passwords[class_name]
        class_auth_result = 'valid'if password==password_entered else 'invalid'
        set_variable("CLASS_AUTH_RESULT", class_auth_result)
        set_variable("CLASS_NAME",class_name)
    else:
        set_variable("CLASS_AUTH_RESULT", "invalid")

def identify_class(callerid_num):
    pjsip_json = jsonify_pjsip('/etc/asterisk/pjsip.conf')
    class_mapping = get_class_mapping(pjsip_json)
    user_class = get_user_class(callerid_num, class_mapping)
    return user_class

if __name__ == "__main__":
    main()
