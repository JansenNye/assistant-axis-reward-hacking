"""Verify and optionally extract the recovered cohort episodes (standard library only)."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', type=Path, help='New destination directory')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'published/episode-manifest.json').read_text())
    archive = ROOT/'published'/manifest['archive']
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['sha256']:
        raise ValueError('Episode archive checksum mismatch')
    expected = {'rh_hillclimb/'+f['path']:f for f in manifest['files']}
    if len(expected) != len(manifest['files']):
        raise ValueError('Duplicate manifest paths')
    if args.extract:
        args.extract.mkdir(parents=True, exist_ok=False)
    seen = set()
    episodes = verdicts = 0
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar:
            path = PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or '..' in path.parts or member.name in seen:
                raise ValueError(f'Unsafe or duplicate member: {member.name}')
            data = tar.extractfile(member).read()
            f = expected.get(member.name)
            if f is None or len(data) != f['bytes'] or hashlib.sha256(data).hexdigest() != f['sha256']:
                raise ValueError(f'File integrity mismatch: {member.name}')
            seen.add(member.name)
            if '/runs/' in member.name and member.name.endswith('.jsonl') and not member.name.endswith('_reasoning.jsonl'):
                episodes += len(data.splitlines())
            if '/verdicts/' in member.name:
                verdicts += len(data.splitlines())
            if args.extract:
                target = args.extract/member.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
    if seen != expected.keys() or episodes != manifest['episodes'] or verdicts != manifest['verdict_rows']:
        raise ValueError('Archive inventory or record-count mismatch')
    print(f'Verified {len(seen)} files, {episodes} episodes and {verdicts} recorded judge decisions.')
    print('See docs/EPISODES.md to reconstruct the exact 824 extraction transcripts.')


if __name__ == '__main__':
    main()
