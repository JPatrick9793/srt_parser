"""
Python script to re-write .SRT files with new timestamps
"""

import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta


def parse(input_file: Path, output_file: Path, ms: int):
    """
    re-write the .SRT file with modified timestamp values

    :param ms: (int) time in milliseconds to add/remove from timestamp
    :param input_file: pathlib.Path object to input .SRT file
    :param output_file: pathlib.Path object to new output .SRT file
    """
    delta = timedelta(milliseconds=ms)
    # base = datetime(1990, 1, 1).date()

    r = re.compile(r'^(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)$')
    # td_re = re.compile(r'^(\d\d):(\d\d):(\d\d),(\d\d\d)')

    # open input file
    with input_file.open('r') as fin:
        # open output file
        with output_file.open('w') as fout:
            # iterate over input file lines
            for i, line in enumerate(fin):
                # check for regex pattern
                m = r.match(line)
                if m:
                    # if regex match, parse info
                    str_start, str_end = m.groups()
                    # create the new line
                    new_line = reformat_line(delta, str_end, str_start)
                    # write to output file
                    fout.write(new_line)

                else:
                    # no match, simply copy line
                    fout.write(line)


def reformat_line(delta, str_end, str_start):
    """
    Given the start and end time stamps, rewrite the .SRT line with modified values
    :param delta:
    :param str_end:
    :param str_start:
    :return:
    """
    t_start = datetime.strptime(f'1990-01-02 {str_start}', "%Y-%m-%d %H:%M:%S,%f")
    t_end = datetime.strptime(f'1990-01-02 {str_end}', "%Y-%m-%d %H:%M:%S,%f")
    # add the time delta
    t_start += delta
    t_end += delta
    # reformat the new timestamp line
    new_start: str = t_start.strftime("%H:%M:%S,%f")[:-3]
    new_end: str = t_end.strftime("%H:%M:%S,%f")[:-3]
    new_line: str = f"{new_start} --> {new_end}\n"
    return new_line


def print_first_n_lines(path_to_file: Path, n: int):
    """
    prints the first N lines of a pathlib.Path object

    :param path_to_file: pathlib.Path object to input file
    :param n: number of lines to print
    :return:
    """

    # read out the first 20 lines of the old file
    with path_to_file.open('r') as f:
        for i, line in enumerate(f):
            if len(line.strip()) > 0:
                print(line)
            if i >= n:
                break


def main(in_file: str, out_file: str, suffix: str, milliseconds: int):

    input_file: Path = Path(in_file).resolve()
    assert input_file.exists(), f"Path to input file does not exist: {input_file}"

    # figure out the output file
    if out_file is not None:
        output_file: Path = Path(out_file).resolve()
    else:
        output_file: Path = input_file.with_name(f"{input_file.stem} Copy{input_file.suffix}")

    # (Optional) Add language suffix to end of file name
    if suffix is not None:
        output_file = input_file.with_name(f"{output_file.stem}.{suffix}{output_file.suffix}")

    # # read first N lines from old file
    # print_first_n_lines(path_to_file=input_file, n=20)

    # re-write old file
    parse(input_file=input_file, output_file=output_file, ms=milliseconds)

    # # read for N lines from new file
    # print_first_n_lines(path_to_file=output_file, n=20)


if __name__ == "__main__":

    # parse CLI args
    parser = argparse.ArgumentParser(description='Modify the timestamps on .SRT files.')
    parser.add_argument('--inFile', help='an integer for the accumulator')
    parser.add_argument('-o', '--outFile', help='sum the integers (default: find the max)')
    parser.add_argument('--milliseconds', type=int, help='Time in milliseconds to change the timestamps.')
    parser.add_argument('-s', '--suffix',
                        help="(optional) add a suffix (e.g. 'en') to the file before the .srt extension.")
    args = parser.parse_args()

    inFile = args.inFile
    outFile = args.outFile
    fileSuffix = args.suffix
    tMilliseconds = args.milliseconds

    main(in_file=inFile, out_file=outFile, suffix=fileSuffix, milliseconds=tMilliseconds)
