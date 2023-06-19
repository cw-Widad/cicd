#!/usr/bin/python3
import os
import argparse
import stat
def longformat(filepath):
    path = os.path.abspath(filepath)
    filelist = os.listdir(filepath)
    #[print(os.path.join(path,i)) for i in filelist]
    for i in filelist:
        abspath = os.path.join(path,i)
        stats = os.stat(abspath)
        if not i.startswith('.'):
           print(f"{stat.filemode(stats.st_mode)} {stats.st_nlink}      {stats.st_uid}       {stats.st_gid}       {stats.st_size}        {stats.st_atime}      {i}")

def hiddenfiles(filepath):
    for root, dirs, files in os.walk(filepath):
        for file in files:
            print(file)
def recursivels(filepath):
    for root, dirs, files in os.walk(filepath):
            for file in files:
                if not file.startswith('.'):
                    print(os.path.join(root, file))

def main():
    parser = argparse.ArgumentParser()
    # Add optional arguments
    parser.add_argument("filepath", help="path to list files",
                        type=str,default=".",nargs='?')
    parser.add_argument( '-a', help ="list all including hidden files",action="store_true")
    parser.add_argument('-l', help = "list in long format",action="store_true")
    parser.add_argument('-R',help = "list recursively",action="store_true")

    #parser.add_argument('-h', help = "ls program in python")
    # Parse arguments from terminal
    args = parser.parse_args()
    if args.l:
        longformat(args.filepath)
    elif args.a:
        hiddenfiles(args.filepath)
    elif args.R:
        recursivels(args.filepath)
    else:
        [ print(f"\'{i}\'" if ' ' in i else f"{i}")for i in os.listdir(args.filepath)]


if __name__ == "__main__":
    main()