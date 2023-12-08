from sshcheckers import ssh_checkout, upload_files
import yaml
import pytest
import random, string

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

@pytest.fixture(scope='class')
def create_deploy():
    res = []
    upload_files(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                 f'{data.get("folder_in")}{data.get("file")}.deb',
                 f'{data.get("path_user")}{data.get("file")}.deb')
    res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                            f'echo {data.get("pswd")} | sudo -S dpkg -i {data.get("path_user")}{data.get("file")}.deb'))
    res.append(ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                            f'echo {data.get("pswd")} | sudo -S dpkg -s {data.get("file")}',
                            "Status: install ok installed"))
    return all(res)



@pytest.fixture(scope='class')
def make_folders():
    return ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                        f'mkdir -p {data.get("folder_user_in")} {data.get("folder_user_out")} {data.get("folder_user_ex")}',
                        '')


@pytest.fixture(scope='class')
def delete_folders():
    yield
    return ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                        f'rm -rf {data.get("folder_user_in")} {data.get("folder_user_out")} {data.get("folder_user_ex")}',
                        '')


@pytest.fixture(scope='class')
def make_files():
    list_off_files = []
    for i in range(data.get("count")):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                        f' cd {data.get("folder_user_in")}; dd if=/dev/urandom of={filename} bs={data.get("bs")} count=1',
                        ''):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture(scope='class')
def delete_deploy():
    yield
    return ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                        f'echo {data.get("pswd")} | sudo -S dpkg -r {data.get("file")}')