from __future__ import print_function

import sys
from graph import *
from timer import *


def conv(token):
    try:
        return int(x=token)
    except:
        return "Not an int"

def main():
    if len(sys.argv) == 1:
        try:
            prufer = list()
            line = None
            nums = list()
            vals = None

            while True:
                line = sys.stdin.readline()
                try:
                    vals = str(line).split(" ")
                    if len(vals) == 0 or vals[0] == "":
                        break
                    nums = map(conv, vals)
                    for i in nums:
                        if type(i) != int:
                            nums.remove(i)
                    if len(nums) == 0:
                        break
                    for i in nums:
                        prufer.append(i)

                except Exception as ex:
                    print("Main Error", ex.message)
                    raise ex

            graph = Graph(len(prufer) + 2, 0, False, True)

            graph.buildFromPrufer(prufer)


        except Exception as ex:
            raise ex
    else:
        print("Do not supply any arguments.")

main()
