"""Prepare a minimal observation bundle from complete caches, without generated code.

This only writes local files. Confirm artifact distribution rights and choose a data
license before publishing the output directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from axis_rh.correlation.analyze import binary_outcome
from axis_rh.correlation.random_vector_analysis import load_cache

RECORD_FIELDS = ('example_id', 'scenario', 'turn', 'status', 'residuals',
                 'region_counts', 'prompt_tokens', 'response_tokens')
OUTCOME_FIELDS = ('example_id', 'scenario', 'status', 'label', 'model_key', 'verdict',
                  'strength', 'stratum', 'problem', 'run_family', 'episode_id', 'harness_label')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories', nargs='+', type=Path)
    parser.add_argument('--axis', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    records, _ = load_cache(args.directories)
    if args.out.exists():
        parser.error('Output must be a new directory')
    # A verdict is required so removing final_code cannot change the fallback label rule.
    if any(r['outcome'].get('verdict') is None for _, r in records):
        parser.error('Every outcome needs an explicit verdict before final_code can be removed')
    args.out.mkdir(parents=True)
    by_directory = {}
    for directory, record in records:
        by_directory.setdefault(directory, []).append(record)
    for directory, rows in by_directory.items():
        identity = json.loads((directory / 'manifest.json').read_text())['identity']
        dest = args.out / 'artifacts' / 'cache' / f'shard_{identity["shard"]}'
        dest.mkdir(parents=True)
        shutil.copyfile(directory / 'manifest.json', dest / 'manifest.json')
        with (dest / 'records.jsonl').open('w') as out:
            for record in rows:
                public = {k: record[k] for k in RECORD_FIELDS if k in record}
                public['outcome'] = {k: record['outcome'][k] for k in OUTCOME_FIELDS if k in record['outcome']}
                if binary_outcome(public['outcome']) != binary_outcome(record['outcome']):
                    raise ValueError('Removing outcome metadata changed classification')
                relative = Path(record['residuals'])
                if relative.is_absolute() or '..' in relative.parts:
                    raise ValueError('Residual path must stay inside its shard')
                (dest / relative).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(directory / relative, dest / relative)
                out.write(json.dumps(public) + '\n')
    shutil.copyfile(args.axis, args.out / 'artifacts' / 'assistant_axis.pt')
    files = [{'path': str(p.relative_to(args.out)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
              'bytes': p.stat().st_size} for p in sorted(args.out.rglob('*')) if p.is_file()]
    manifest = {'schema': 1, 'observations': len(records),
                'transformation': 'Generated code and unused outcome metadata removed; activations, axis and scoring inputs unchanged.',
                'files': files}
    (args.out / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Prepared {len(records)} observations at {args.out}; no upload performed.')


if __name__ == '__main__':
    main()
