#!/usr/bin/env python3

import sys
import subprocess
import re
from collections import defaultdict

def line_is_context(l):
    l = l.strip()
    if len(l) < 3:
        return (False, '')
    if l[0] == '[' and l[1] != ']':
        ctxt = l[1:].split(']')[0]
        return (True, ctxt)
    return (False, '')

def is_template(context_name):
	is_tmp = ('(!' in context_name or ',!' in context_name) and context_name.strip().endswith(')')
	return is_tmp

def jsonify_pjsip(pathtopjsip):
    with open(pathtopjsip, 'r') as pjsip_file:
        pjsip_lines = pjsip_file.readlines()

    pjsip_json = defaultdict(dict)
    current_context = None

    list_of_context = [line_is_context(line.strip())[1] for line in pjsip_lines if line_is_context(line)[0] and not line.strip().startswith(';')]

    for line in pjsip_lines:
        line = line.strip()
        if line.startswith(';') or not line:
            continue

        is_context, context_name = line_is_context(line)
        if is_context:
            base_context_name = line.split('(')[0]
            inheritance_info = line.split('(')[-1].rstrip(')')
            
            current_context = base_context_name
            pjsip_json[current_context]['is_template'] = is_template(line)
            
            if ',' in inheritance_info:
                if 'inherits_from' in pjsip_json[current_context]:
                    pjsip_json[current_context]['inherits_from'] += [inh.strip() for inh in inheritance_info.split(',')]
                else:
                    pjsip_json[current_context]['inherits_from'] = [inh.strip() for inh in inheritance_info.split(',')]
            elif inheritance_info and inheritance_info != '!':
                if 'inherits_from' in pjsip_json[current_context]:
                    pjsip_json[current_context]['inherits_from'] += [inheritance_info.strip()]
                else:
                    pjsip_json[current_context]['inherits_from'] = [inheritance_info.strip()]
            else:
                if 'inherits_from' not in pjsip_json[current_context]:
                    pjsip_json[current_context]['inherits_from'] = []
        else:
            if current_context:
                key_value_match = re.match(r'(\S+)\s*=\s*(\S+)', line)
                if key_value_match:
                    key, value = key_value_match.groups()
                    is_value_context = value in list_of_context
                    pjsip_json[current_context][key] = (value, is_value_context)

    return pjsip_json


def get_class_mapping(pjsip_json):
    class_mapping = {}

    for context, attributes in list(pjsip_json.items()):
        if 'context' in attributes and attributes.get('context')[0] in ['etudiant', 'delegue']:
            for inherited_context in attributes.get('inherits_from', []):
                inherited_context = inherited_context.lstrip('!')
                if f'[{inherited_context}]' in pjsip_json.keys():
                    inherited_attributes = pjsip_json[f'[{inherited_context}]']
                    if inherited_attributes.get('is_template', False) and 'context' in inherited_attributes.keys():
                        class_name = inherited_attributes['context'][0]
                        class_mapping[context] = class_name.split('_')[0].strip()
                else:print('bad template......')
                        
    return class_mapping

def set_variable(name, value):
    command = f"perl /var/lib/asterisk/agi-bin/save_var.pl {name} {value}"
    subprocess.run(command, shell=True)

def get_user_class(callerid_num, class_mapping):
    return class_mapping.get(f'[{callerid_num}]', "Unknown")

def main():
    
    callerid_num = sys.argv[1] if len(sys.argv) > 1 else None

    if not callerid_num:
        sys.stderr.write("Erreur: Numéro de l'appelant non fourni.\n")
        return

    pjsip_json = jsonify_pjsip('/etc/asterisk/pjsip.conf')
    class_mapping = get_class_mapping(pjsip_json)
    user_class = get_user_class(callerid_num, class_mapping)

    # Définir la variable USER_CLASS avec la classe trouvée
    set_variable("USER_CLASS", user_class)

if __name__ == "__main__":
    main()
