from fabric import Connection


def copy_script():
    # Replace 'your_local_path' with the local path to your script
    local_path = '/home/yk/Desktop/ALX/AirBnB_clone_v2/0-setup_web_static.sh'

    # Replace 'your_remote_path' with the remote path on the server
    remote_path = '/home/ubuntu/0-setup_web_static.sh'

    # Replace 'your_username' with the SSH username for the remote server
    username = 'ubuntu'

    # Remote server
    hosts = ['52.23.178.146', '100.26.223.57']

    for host in hosts:
        # Connect to the remote server
        with Connection(host=host, user=username) as c:
            # Upload the script to the remote server
            c.put(local_path, remote_path)


if __name__ == "__main__":
    copy_script()
