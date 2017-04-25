from compotia.watch.dog import Dog
from compotia.transpiler.transpiler import Transpiler
import argparse


parser = argparse.ArgumentParser()


def run():
    parser.add_argument('--watch')
    parser.add_argument('-i')
    parser.add_argument('-o')
    args = parser.parse_args()

    if not args.watch:
        if not args.i:
            args.i = './config.json'
        if not args.o:
            args.o = '.'

        transpile(args.i, args.o)

def transpile(in_path, out_path):
    transpiler = Transpiler()
    transpiler.transpile(in_path, out_path)

def watch(in_path):
    dog = Dog()
    dog.watch(in_path, out_path)
