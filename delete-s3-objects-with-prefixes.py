import argparse
import subprocess
import os
import sys
import textwrap


def delete_s3_objects(bucket, prefixes, live):
    try:
        term_width = os.get_terminal_size().columns
    except OSError:
        term_width = 80  # or whatever default width you want to use

    print(f"🪣  Target Bucket: {bucket}", file=sys.stderr)
    print(f"🗂️  Target Prefixes: {textwrap.fill(', '.join(prefixes.split(',')),
          width=term_width)}",file=sys.stderr)
    print(f"🌵 Is dryrun: {'No (⚠️  This is live. Proceed with caution.)' if live else 'Yes (Not actually deleting the objects.)'}",
          file=sys.stderr)
    print("\nAre you sure you want to continue deleting objects? [y/N]: ", end='', file=sys.stderr)
    proceed = input()
    if proceed.lower() != 'y':
        print("Operation cancelled.", file=sys.stderr)
        return

    for prefix in prefixes.split(','):
        base_command = ['aws', 's3', 'rm',
                        f's3://{bucket}/{prefix}', '--recursive']
        if not live:
            base_command.append('--dryrun')

        print(f"\nExecuting {' '.join(base_command)}\n")

        result = subprocess.run(base_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(
                f"An error occurred while deleting objects from prefix {prefix}:")
            print(result.stderr)
        else:
            print(result.stdout)


def main():
    parser = argparse.ArgumentParser(
        description='Delete S3 objects with specific prefixes.')
    parser.add_argument('bucket', type=str, help='Target bucket')
    parser.add_argument('prefixes', type=str,
                        help='Target prefixes, comma-separated. Each prefix starts without a slash. Example: folder1/folder2,folder3/folder4')
    parser.add_argument('--live', action='store_true', help='Enable live run')
    args = parser.parse_args()
    delete_s3_objects(args.bucket, args.prefixes, args.live)


if __name__ == "__main__":
    main()
