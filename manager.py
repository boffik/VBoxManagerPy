import subprocess as sp
import sys
import argparse

#list of commands
cmd_vmlist  = 'VBoxManage list vms'
cmd_vminfo  = 'VBoxManage showvminfo %s --machinereadable'
cmd_stopvm  = 'VBoxManage controlvm %s poweroff'
cmd_startvm = 'VBoxManage startvm %s --type headless'
cmd_resetvm = 'VBoxManage controlvm %s reset'
#list of user input actions
user_acts = ["start", "stop", "reset"]

def print_allvms_state(list):
    j = 0
    for item in list:
        j += 1
        vm = get_vminfo(item)
        print('%d: VM "%s" is %s' % (j, vm['name'], vm['VMState']))

def check_allvms_state():
    ret = []
    if list_vm is not None:
        j = 0
        for key in sorted(list_vm.keys()):
            j += 1;
            ret.append(list_vm[key])
    else:
        print('No VMs available for this user.')
    return(ret, j)

def __check_property__(uiid,prop):
    return get_vminfo(uiid)[prop]

def restart_vm(uiid):
    cmd = cmd_resetvm % (uiid)
    return __shell_cmd_wo__(cmd)

def start_vm(uiid):
    cmd = cmd_startvm % (uiid)
    return __shell_cmd_wo__(cmd)

def stop_vm(uiid):
    state = __check_property__(uiid,'VMState')
    if state != 'poweroff':
        cmd = cmd_stopvm % (uiid)
        __shell_cmd_wo__(cmd)
        print('VM "%s" has been stoped.' % uiid)
    else:
        print('VM is already %s' % state)

def get_vminfo(uiid):
    cmd = cmd_vminfo % (uiid)
    return __get_cmd__(cmd, '=')

def get_vmlist():
    return __get_cmd__(cmd_vmlist, ' ')

def __get_cmd__(cmd,sep):
    list = dict()
    __shell_cmd__(cmd,list,sep)
    if len(list) > 0:
        return list
    else:
        print('No output from cmd \'%s\'' % cmd)

def __shell_cmd__(cmd,list,sep):
    PIPE = sp.PIPE
    p = sp.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=sp.STDOUT, close_fds=True)

    while True:
        s = p.stdout.readline().decode('utf-8').replace('"','').replace('{','').replace('}','')
        new = s[:len(s)-1].split(sep)
        if new[0] == '':
            break
        else:
            list[new[0]] = new[1]

def __shell_cmd_wo__(cmd, output=True):
    PIPE = sp.PIPE
    p = sp.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=sp.STDOUT, \
        close_fds=True).stdout.readlines()
    if output:
        for i in p:
            print(i.decode('utf-8').replace('\n','').split(': ')[-1])

def print_info():
    print('- ' * 15)
    print('VirtualBox VMs state:')
    print('- ' * 15)
    print_allvms_state(p[0])
    print()

def start_program():
    print_info()
    print("Please type an action %s with VM or 'exit' to close program" % ('|'.join(user_acts)))
    act = str(input('> '))
    if act == 'exit':
        sys.exit()

    print("Please type a number VM")
    num = int(input('> '))
    if num > 0 and num <= p[1]:
        if act in user_acts:
            do_actions_vm([num], act)
        else:
            print('You are enter a wrong action.')
    else:
        print('You are enter a wrong VM number.')


def do_actions_vm(id_list, action):
    for id in id_list:
        if action == 'start':
            start_vm(p[0][id-1])
        elif action == 'stop':
            stop_vm(p[0][id-1])
        elif action == 'reset':
            restart_vm(p[0][id-1])


def args_parse():
    parser=argparse.ArgumentParser(description='VboxManagerPy script',add_help=False)
    parser.add_argument('-a', '--action', choices=user_acts, help='type an action with VMs')
    parser.add_argument('--id', metavar='id', nargs='*', type=int, help='type a VM number or VM numbers through space')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='print a list of VMs')
    return parser

if __name__ == '__main__':
    ap = args_parse()
    args = ap.parse_args()
    list_vm = get_vmlist()
    p = check_allvms_state()

    if args.list:
        print_info()
    elif args.id or args.action:
        if args.id:
            do_actions_vm(args.id, args.action)
        else:
            print('manager.py: error: use --id argument with --action.')
            ap.print_help()
    else:
        start_program()
