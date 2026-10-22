"""Verify exact extraction transcripts and their join to the published observations."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def key(row):
    return row['example_id'], row['scenario'], row['turn']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write original JSONL to a new file for extraction')
    parser.add_argument('--cache', type=Path, help='Optional downloaded cache directory containing shard_*/')
    args = parser.parse_args()
    published = ROOT/'published'
    manifest = json.loads((published/'transcript-manifest.json').read_text())
    compressed = (published/manifest['archive']).read_bytes()
    if hashlib.sha256(compressed).hexdigest() != manifest['archive_sha256']:
        raise ValueError('Compressed transcript checksum mismatch')
    raw = gzip.decompress(compressed)
    if hashlib.sha256(raw).hexdigest() != manifest['transcripts_sha256']:
        raise ValueError('Extraction-input checksum mismatch')
    records = [json.loads(line) for line in raw.splitlines()]
    actual = {key(row):row for row in records}
    if len(actual) != len(records) or len(actual) != manifest['observations']:
        raise ValueError('Duplicate or missing transcripts')
    index = (published/'transcript-observations.json').read_bytes()
    if hashlib.sha256(index).hexdigest() != manifest['observation_index_sha256']:
        raise ValueError('Observation-index checksum mismatch')
    observations = json.loads(index)
    if args.cache:
        observations = []
        shards = sorted(args.cache.glob('shard_*/manifest.json'))
        if len(shards) != 6:
            raise ValueError('Expected all six cache shards')
        for path in shards:
            identity = json.loads(path.read_text())['identity']
            if identity['transcripts_sha256'] != manifest['transcripts_sha256']:
                raise ValueError(f'Cache names a different extraction input: {path}')
            observations.extend(json.loads(line) for line in (path.parent/'records.jsonl').read_text().splitlines())
    expected = {key(row):row for row in observations}
    if len(expected) != len(observations) or expected.keys() != actual.keys():
        raise ValueError('Transcript and observation IDs differ')
    for identity, observation in expected.items():
        for field, value in observation['outcome'].items():
            if actual[identity]['outcome'].get(field) != value:
                raise ValueError(f'Outcome mismatch: {identity}, {field}')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as output:
            output.write(raw)
    print(f'Verified {len(records)} exact extraction transcripts and matching observation outcomes.')
    print(f'Original extraction-input SHA-256: {manifest["transcripts_sha256"]}')
    print('Recorded verdicts are preserved; this is not an independent rejudging of hacking.')


if __name__ == '__main__':
    main()
