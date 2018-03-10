import tinify
import config
import os.path
import os
import sys

tinify.key = config.SECRET
compressdir = '/Volumes/work/tinypng/'
sourcedir = '/Volumes/work/pngsource/'

def compress(sourcepath,compresspath):
    files = os.listdir(sourcepath)
    for fi in files:
        fi_d = os.path.join(sourcepath, fi)
        if os.path.isdir(fi_d):
            compress_d = os.path.join(compresspath, fi)
            os.makedirs(compress_d)
            compress(fi_d,compress_d)
        else:
            #print os.path.join(compresspath,fi)
            path = os.path.join(sourcepath,fi)
            compress_path = os.path.join(compresspath,fi)
            if path.endswith('.png'):
                source = tinify.from_file(os.path.join(os.path.join(sourcepath, fi)))
                source.to_file(os.path.join(os.path.join(compresspath, fi)))


if __name__ == '__main__':
    print compress(sourcedir,compressdir);