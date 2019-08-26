#! /usr/bin/env python3

import argparse


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="View turns from a game playback JSON file")
    
    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        'play_file', type=argparse.FileType('r'),
         help='The file to open')
    # parser.add_argument(
    #     '--log', default=sys.stdout, type=argparse.FileType('w'),
    #     help='the file where the sum should be written')
    args = parser.parse_args()
    print('%s' % args.play_file.read())
    main()
