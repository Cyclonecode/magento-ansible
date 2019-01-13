#!/usr/bin/python

# Copyright: (c) 2018, Krister Andersson
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: magento
version_added: '2.7.5'
short_description: Execute magento commands.
description:
- Execute magento commands.
options:
  command:
    description:
    - The command to execute.
    aliases: [ action ]
    required: yes
  cwd:
    description:
    - Path to magento.
  version:
    description:
    - Magento version.
    choices: [ 1, 2 ]
    default: 2

'''

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

def run_magento(module, cmd):
    try:
      (rc, out, err) = module.run_command((cmd))
    except Exception as e:
      module.fail_json(msg=to_native(e))

    if rc != 0:
      module.fail_json(msg=to_native("Command %s failed with error code %d") %(cmd, rc))

    return rc, ' '.join(out.splitlines()), err

def main():
    module = AnsibleModule(
        argument_spec = dict(
            command     = dict(aliases=['action']),
            cwd         = dict(type='path'),
            version     = dict(default='2')
        )
    )
    command = module.params.get('command')
    cwd = module.params.get('cwd')
    version = module.params.get('version')

    m = ""

    if cwd:
      try:
        chdir = os.path.abspath(cwd)
        os.chdir(cwd)
      except Exception as e:
        module.fail_json(msg=to_native(e))


    rc, out, err = run_magento(module, "bin/magento %s" %(command))

    module.exit_json(version=version, command=command, msg=out, rc=rc, changed=True)

if __name__ == '__main__':
    main()
