import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_http(host):
    cmd = host.run('curl http://localhost')
    assert cmd.rc == 0
    assert "<html><h1>Hello World</h1></html>" in cmd.stdout
