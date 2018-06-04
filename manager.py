import subprocess as sp
import sys

#list of commands
cmd_vmlist  = 'VBoxManage list vms'
cmd_vminfo  = 'VBoxManage showvminfo %s --machinereadable'
cmd_stopvm  = 'VBoxManage controlvm %s poweroff'
cmd_startvm = 'VBoxManage startvm %s --type headless'
cmd_resetvm = 'VBoxManage controlvm %s reset'
#list of user input actions
user_acts = ["'start'", "'stop'", "'reset'"]

def check_allvms_state():
    ret = []
    if list_vm is not None:
        j = 0
        for key in sorted(list_vm.keys()):
            j += 1;
            ret.append(list_vm[key])
            print('%d: VM "%s" is %s' % (j, key, __check_property__(list_vm[key],'VMState')))
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
        if len(s) == 0:
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

list_vm = get_vmlist()

def start_program():
    print('VirtualBox VMs state:')
    print()
    p = check_allvms_state()
    print()
    print("Please type an action %s with VM or 'exit' to close program" % ('|'.join(user_acts)))
    act = str(input('> '))
    if act == 'exit':
        sys.exit()

    print("Please type a number VM")
    num = int(input('> '))
    if num > 0 and num <= p[1]:
        if act == 'start':
            start_vm(p[0][num-1])
        elif act == 'stop':
            stop_vm(p[0][num-1])
        elif act == 'reset':
            restart_vm(p[0][num-1])
        else:
            print('You are enter a wrong action.')
    else:
        print('You are enter a wrong VM number.')


if __name__ == '__main__':
    argv = [str(arg) for arg in sys.argv[1::2]]
    if len(argv) % 2 == 1:
        print(argv)
    elif len(argv) == 0:
        start_program()
    else:
        print('Wrong arguments')

