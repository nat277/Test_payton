from sshcheckers import ssh_checkout
import yaml
import pytest

with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)


@pytest.mark.usefixtures('create_deploy', 'make_folders', 'make_files', 'delete_folders', 'delete_deploy')
class TestHW:

    def test_step_1(self):
        assert ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                            f'cd {data.get("folder_user_in")}; 7z -t{data.get("type")} a {data.get("folder_user_out")}/archive_1',
                            'Everything is Ok')

    def test_step_2(self):
        assert ssh_checkout(f'{data.get("host")}', f'{data.get("user")}', f'{data.get("pswd")}',
                            f'cd {data.get("folder_user_out")}; 7z x archive_1.{data.get("type")} -o{data.get("folder_user_ex")} -y',
                            'Everything is Ok')


if __name__ == '__main__':
    pytest.main(['-vv'])