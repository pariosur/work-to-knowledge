#!/usr/bin/env python3
"""Optional isolated Pi CLI install/discovery check; never prompts a model or records notes."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def check(source):
    pi = shutil.which('pi')
    if not pi:
        raise SystemExit('Pi CLI unavailable; no runtime test performed')
    with tempfile.TemporaryDirectory(prefix='wtk-pi-') as directory:
        temp = Path(directory)
        home, agent, cwd = (temp / name for name in ('home', 'agent', 'work'))
        for path in (home, agent, cwd):
            path.mkdir()
        # Keep platform/network routing only, not provider keys, Pi settings, or the user's HOME.
        env = {key: os.environ[key] for key in ('PATH', 'SystemRoot', 'COMSPEC', 'PATHEXT',
                                                    'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
                                                    'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy') if key in os.environ}
        env.update(HOME=str(home), USERPROFILE=str(home), PI_CODING_AGENT_DIR=str(agent),
                   PI_CODING_AGENT_SESSION_DIR=str(temp / 'sessions'), PI_OFFLINE='1',
                   PI_SKIP_VERSION_CHECK='1', PI_TELEMETRY='0',
                   npm_config_cache=str(temp / 'npm-cache'), GIT_TERMINAL_PROMPT='0')
        def run(*args):
            result = subprocess.run([pi, *args], env=env, cwd=cwd,
                                    text=True, capture_output=True, timeout=180)
            if result.returncode:
                raise RuntimeError(f'Pi {args[0]} failed: {result.stdout}\n{result.stderr}')
            return result.stdout
        print('Pi ' + run('--version').strip())
        run('install', source)
        assert source in run('list')
        settings = json.loads((agent / 'settings.json').read_text())
        assert len(settings['packages']) == 1, settings
        installed_source = settings['packages'][0]
        if Path(source).is_absolute():
            assert (agent / installed_source).resolve() == Path(source).resolve(), settings
        else:
            assert installed_source == source, settings
        with (temp / 'rpc.log').open('w') as log:
            process = subprocess.Popen([pi, '--mode', 'rpc', '--no-session', '--no-tools',
                                        '--no-extensions', '--no-context-files', '--offline'],
                                       env=env, cwd=cwd, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=log, text=True)
            selector = selectors.DefaultSelector()
            selector.register(process.stdout, selectors.EVENT_READ)
            try:
                process.stdin.write(json.dumps({'id': 'wtk-check', 'type': 'get_commands'}) + '\n')
                process.stdin.flush()
                deadline = time.monotonic() + 45
                result = None
                while time.monotonic() < deadline:
                    if selector.select(timeout=1):
                        line = process.stdout.readline()
                        if not line:
                            raise RuntimeError('Pi exited: ' + (temp / 'rpc.log').read_text())
                        message = json.loads(line)
                        if message.get('id') == 'wtk-check':
                            assert message['success'], message
                            result = message['data']
                            break
                assert result is not None, 'Pi RPC get_commands timed out'
                skills = [c for c in result['commands'] if c['source'] == 'skill']
                assert [c['name'] for c in skills] == ['skill:work-to-knowledge'], skills
                info = skills[0]['sourceInfo']
                assert info['origin'] == 'package', info
                skill = Path(info['path'])
                assert skill.is_file(), skill
                base = skill.parent
                assert 'references/setup.md' in skill.read_text()
                assert '/skill:work-to-knowledge Run the one-time setup for Pi.' in (base / 'references/setup.md').read_text()
                for relative in ('references/harnesses.md', 'scripts/loop_state.py', 'assets/config.example.json', 'LICENSE'):
                    assert (base / relative).is_file(), relative
                spec = importlib.util.spec_from_file_location('installed_loop_state', base / 'scripts/loop_state.py')
                helper = importlib.util.module_from_spec(spec)
                sys.dont_write_bytecode = True
                spec.loader.exec_module(helper)
                config = json.loads((base / 'assets/config.example.json').read_text())
                assert not config['enabled'] and config['sources'] == []
                store = temp / 'notes'
                config['store'] = str(store)
                context = {'roots': [str(cwd)], 'topics': [], 'scope_known': True, 'no_record': False}
                assert not helper.gate(config, context, temp)
                config['enabled'] = True
                config['scope'] = {'mode': 'project', 'roots': [str(cwd)], 'topics': [],
                                   'exclude_roots': [], 'exclude_topics': []}
                assert helper.gate(config, context, temp)
                assert not helper.gate(config, dict(context, no_record=True), temp)
                assert not helper.gate(config, dict(context, scope_known=False), temp)
                config['scope']['exclude_roots'] = [str(cwd)]
                assert not helper.gate(config, context, temp)
                assert not store.exists()
                assert not any(cwd.iterdir())
                print('PASS: package install/list and exactly one package skill in fresh Pi RPC inventory')
                print('PASS: bundled setup route/resources and read-only disabled, allowed, excluded, ambiguous, no-record gates')
                print('No model call, journal write, or active user configuration change performed')
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default=str(ROOT), help='Local package path or authorized git package source')
    args = parser.parse_args()
    check(args.source)
