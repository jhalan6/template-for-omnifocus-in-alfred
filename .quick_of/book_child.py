# -*- coding:utf-8 -*-
import sys


def main():
    """
        This is a little script to generate a book list
    """
    chapter_count = sys.argv[1]
    for chapter in range(1, int(chapter_count) + 1):
        print "Chapter %d" % chapter


if __name__ == "__main__":
        main()
