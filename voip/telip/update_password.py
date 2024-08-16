#!/usr/bin/env python3
import sys
import os

def line_is_context(l):
    l=l.strip()
    if len(l)<3:
        return (False,'')
    if l[0]=='[' and l[1]!=']':
        ctxt = l[1:].split(']')[0]
        return (True,ctxt)
    return (False,'')


def update_password(auth_section, new_password):
    conf_file = '/etc/asterisk/pjsip.conf'
    with open(conf_file, 'r') as file_r:
        lines = file_r.readlines()
    with open(conf_file, 'w') as file_w:
        last_context = ''
        for line in lines:
            line_is_ctx,context = line_is_context(line)
            if line_is_ctx:
                last_context = context
            else:
                if line.strip().startswith('password=') and last_context==auth_section:
                    file_w.write(f"password={new_password}\n")
                    continue
            file_w.write(line)

    os.system('asterisk -rx "pjsip reload"')

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        sys.stderr.write("Erreur: Ce script nécessite deux arguments.\n")
        return

    callerid_num = args[0]
    new_password = args[1]
    print(f"CallerID: {callerid_num}, New Password: {new_password}")

    # Déterminez la classe de l'utilisateur en fonction de l'extension
    if callerid_num.startswith('6001') or callerid_num.startswith('6002'):
        auth_section = 'L1_class_auth'
    elif callerid_num.startswith('6003'):
        auth_section = 'L2_class_auth'
    elif callerid_num.startswith('6004'):
        auth_section = 'L3_class_auth'
    else:
        sys.stderr.write("Classe non reconnue. Impossible de changer le mot de passe.\n")
        return

    update_password(auth_section, new_password)
    sys.stdout.write("Le mot de passe a été mis à jour avec succès.\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
