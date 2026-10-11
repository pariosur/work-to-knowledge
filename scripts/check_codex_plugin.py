#!/usr/bin/env python3
"""Optional no-model smoke test using an installed Codex CLI and temporary configuration."""
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def check():
    codex = shutil.which('codex')
    if not codex:
        raise SystemExit('Codex CLI unavailable; no runtime test performed')
    with tempfile.TemporaryDirectory(prefix='wtk-plugin-') as directory:
        temp = Path(directory)
        home, codex_home, cwd = (temp / name for name in ('home', 'codex', 'work'))
        for path in (home, codex_home, cwd):
            path.mkdir()
        env = dict(os.environ, HOME=str(home), CODEX_HOME=str(codex_home))
        def run(*args):
            return subprocess.run([codex, *args], env=env, cwd=cwd, check=True,
                                  text=True, capture_output=True, timeout=60).stdout
        print(run('--version').strip())
        run('plugin', 'marketplace', 'add', str(ROOT))
        installed = json.loads(run('plugin', 'add', 'work-to-knowledge@work-to-knowledge', '--json'))
        assert Path(installed['installedPath']).is_relative_to(codex_home)
        listed = json.loads(run('plugin', 'list', '--json', '--marketplace', 'work-to-knowledge'))
        assert len(listed['installed']) == 1 and listed['installed'][0]['enabled']
        with (temp / 'server.log').open('w') as log:
            process = subprocess.Popen([codex, 'app-server', '--stdio'], env=env, cwd=cwd,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=log, text=True)
            selector = selectors.DefaultSelector()
            selector.register(process.stdout, selectors.EVENT_READ)
            def request(i, method, params):
                process.stdin.write(json.dumps({'id': i, 'method': method, 'params': params}) + '\n')
                process.stdin.flush()
                deadline = time.monotonic() + 30
                while time.monotonic() < deadline:
                    if selector.select(timeout=1):
                        line = process.stdout.readline()
                        if not line:
                            raise RuntimeError('App server exited before response')
                        message = json.loads(line)
                        if message.get('id') == i:
                            if 'error' in message:
                                raise RuntimeError(message['error'])
                            return message['result']
                raise TimeoutError(method)
            try:
                request(1, 'initialize', {'clientInfo': {'name': 'wtk_plugin_test', 'version': '0.1.0'},
                                         'capabilities': {'experimentalApi': True}})
                process.stdin.write(json.dumps({'method': 'initialized'}) + '\n')
                process.stdin.flush()
                result = request(2, 'skills/list', {'cwds': [str(cwd)], 'forceReload': True})
                assert len(result['data']) == 1
                data = result['data'][0]
                assert not data['errors'], data['errors']
                skills = [s for s in data['skills'] if s.get('pluginId') == 'work-to-knowledge@work-to-knowledge']
                assert sorted(s['name'] for s in skills) == ['work-to-knowledge:setup', 'work-to-knowledge:work-to-knowledge']
                for skill in skills:
                    assert skill['enabled'] and Path(skill['path']).is_relative_to(codex_home)
                    assert Path(skill['path']).is_file()
                print('PASS: native marketplace install, enabled state, and exactly two cached skills load')
                print('No model request, journal write, or active user configuration change performed')
            finally:
                selector.close()
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                process.stdin.close()
                process.stdout.close()


if __name__ == '__main__':
    check()
