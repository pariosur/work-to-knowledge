"""Read-only scope and checkpoint planning. No recording or filesystem mutations."""
import hashlib
import json
import os
from pathlib import Path
import sys


def resolve(value, base):
    p = Path(value).expanduser()
    return (p if p.is_absolute() else Path(base) / p).resolve()


def validate(c):
    if not isinstance(c, dict) or c.get('version') != 1:
        raise ValueError('unsupported configuration')
    if type(c.get('enabled')) is not bool or not isinstance(c.get('store'), str) or not c['store'].strip():
        raise ValueError('enabled and store required')
    s = c.get('scope', {})
    if not isinstance(s, dict) or s.get('mode') not in ('global', 'project', 'selected'):
        raise ValueError('invalid scope')
    for key in ('roots', 'topics', 'exclude_roots', 'exclude_topics'):
        if not isinstance(s.get(key), list) or any(not isinstance(x, str) or not x.strip() for x in s[key]):
            raise ValueError('scope lists must contain nonempty strings')
    if s['mode'] == 'project' and (len(s['roots']) != 1 or s['topics']):
        raise ValueError('project requires one root and no topics')
    if s['mode'] == 'global' and (s['roots'] or s['topics']):
        raise ValueError('global has no inclusion selectors')
    if s['mode'] == 'selected' and c['enabled'] and not (s['roots'] or s['topics']):
        raise ValueError('selected scope requires an inclusion')
    sources = c.get('sources')
    if not isinstance(sources, list):
        raise ValueError('sources list required')
    for source in sources:
        if not isinstance(source, dict) or source.get('access') not in ('read', 'read_append_links') or not isinstance(source.get('path'), str) or not source['path'].strip():
            raise ValueError('invalid source permission')
    learning = c.get('learning', {})
    if not isinstance(learning, dict) or learning.get('roadmap_mode') not in ('none', 'existing', 'generated'):
        raise ValueError('invalid roadmap mode')
    if not isinstance(learning.get('objective'), str) or not learning['objective'].strip():
        raise ValueError('objective required')
    if not isinstance(learning.get('prerequisites'), list) or any(not isinstance(x, str) for x in learning['prerequisites']):
        raise ValueError('prerequisites list required')
    if type(learning.get('allow_existing_updates')) is not bool:
        raise ValueError('existing update permission required')
    if learning['roadmap_mode'] == 'existing' and (not isinstance(learning.get('existing_path'), str) or not learning['existing_path'].strip()):
        raise ValueError('existing roadmap path required')
    if not isinstance(learning.get('mastery_evidence'), str) or not learning['mastery_evidence'].strip():
        raise ValueError('mastery criterion required')


def gate(config, context, base):
    """Fail closed; path exclusions include every touched root, not just cwd."""
    try:
        validate(config)
        if not isinstance(context, dict) or context.get('no_record') is not False or context.get('scope_known') is not True:
            return False
        if not config['enabled']:
            return False
        roots, topics = context.get('roots'), context.get('topics')
        if not isinstance(roots, list) or not isinstance(topics, list):
            return False
        if any(not isinstance(x, str) or not x.strip() for x in roots + topics):
            return False
        if not roots and not topics:
            return False
        # Context roots must be absolute; don't infer task location from config.
        if any(not Path(x).expanduser().is_absolute() for x in roots):
            return False
        paths = [resolve(x, base) for x in roots]
        if any(not p.exists() or not os.access(p, os.R_OK) for p in paths):
            return False
        s = config['scope']
        within = lambda p, r: p == r or r in p.parents
        excluded = [resolve(x, base) for x in s['exclude_roots']]
        if any(within(p, r) for p in paths for r in excluded) or set(topics) & set(s['exclude_topics']):
            return False
        if s['mode'] == 'global':
            return True
        included = [resolve(x, base) for x in s['roots']]
        # Every touched root must be covered unless the whole task has a selected topic.
        path_match = bool(paths) and all(any(within(p, r) for r in included) for p in paths)
        return path_match or (s['mode'] == 'selected' and bool(set(topics) & set(s['topics'])))
    except (ValueError, TypeError, KeyError, OSError, RuntimeError):
        return False


def episode_id(task_id, event_ids):
    if not isinstance(task_id, str) or not task_id.strip() or not isinstance(event_ids, list) or not event_ids or any(not isinstance(x, str) or not x.strip() for x in event_ids):
        raise ValueError('task and event IDs required')
    raw = json.dumps([task_id, sorted(set(event_ids))], ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


def unreserved(state, event_ids):
    """A prepared transaction reserves events too. Invalid state never resets."""
    if state.get('version') != 1 or not isinstance(state.get('episodes'), dict):
        raise ValueError('invalid state; reconcile existing outputs')
    reserved = set()
    for record in state['episodes'].values():
        if record.get('status') not in ('prepared', 'committed') or not isinstance(record.get('events'), list) or any(not isinstance(x, str) for x in record['events']):
            raise ValueError('invalid episode; reconcile existing outputs')
        reserved.update(record['events'])
    return list(dict.fromkeys(x for x in event_ids if x not in reserved))


def main():
    try:
        command, path, *args = sys.argv[1:]
        c = json.loads(Path(path).read_text())
        if command == 'validate':
            validate(c)
            print('valid')
        elif command == 'gate':
            context = json.loads(Path(args[0]).read_text())
            print('allow' if gate(c, context, Path(path).resolve().parent) else 'skip')
        else:
            raise ValueError('usage: loop_state.py validate CONFIG | gate CONFIG CONTEXT')
    except (ValueError, OSError, IndexError, TypeError):
        if len(sys.argv) > 1 and sys.argv[1] == 'gate':
            print('skip')
        else:
            print('invalid configuration or arguments', file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
