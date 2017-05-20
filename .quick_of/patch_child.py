# -*- coding:utf-8 -*-
import commands


def main():
    """
        generate out put from clipboard
        each line in the clipboard will output in oneline
    """
    (status, output) = commands.getstatusoutput('pbpaste')
    print output


if __name__ == "__main__":
    main()
