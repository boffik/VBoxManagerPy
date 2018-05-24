import subprocess as sp
import sys

def check_allvms_state():
    list_vm = get_vmlist()

    ret = []
    if list_vm is not None:
        j = 0
        for i in sorted(list_vm.keys()):
            j += 1;
            ret.append(list_vm[i])
            print('%d: VM "%s" is %s' % (j, i, __check_property__(list_vm[i],'VMState')))
    else:
        print('No VMs available for this user.')
    return(ret, j)

def __check_property__(uiid,prop):
    return get_vminfo(uiid)[prop]

def start_vm(uiid):
    cmd = 'VBoxManage startvm %s --type headless' % (uiid)
    return __shell_cmd_wo__(cmd)

def stop_vm(uiid):
    cmd = 'VBoxManage controlvm %s poweroff' % (uiid)
    __shell_cmd_wo__(cmd)
    print('VM "%s" has been stoped.' % uiid)

def get_vminfo(uiid):
    cmd = 'VBoxManage showvminfo %s --machinereadable' % (uiid)
    return __get_cmd__(cmd, '=')

def get_vmlist():
    cmd = 'VBoxManage list vms'
    return __get_cmd__(cmd, ' ')

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

def __shell_cmd_wo__(cmd):
    PIPE = sp.PIPE
    p = sp.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=sp.STDOUT, \
        close_fds=True).stdout.readlines()
    for i in p:
        print(i.decode('utf-8').replace('\n',''))

if __name__ == '__main__':
    print('VirtualBox VMs state:')
    print()
    p = check_allvms_state()
    print()
    print("Please type an action 'start'|'stop' with VM or 'exit' to close program")
    act = str(input())
    if act == 'exit':
        sys.exit()

    print("Please type a number VM")
    num = int(input())
    if num > 0 and num < p[1]:
        if act == 'start':
            start_vm(p[0][num-1])
        elif act == 'stop':
            stop_vm(p[0][num-1])
        else:
            print('You are enter a wrong action.')
    else:
        print('You are enter a wrong VM number.')

