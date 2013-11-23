import sys

def print_usage():
    print ('''usage:
thu net
thu net login
thu net logout

thu usereg iplist
thu usereg ipup x.x.x.x
thu usereg ipdown x.x.x.x
thu usereg ipdown 0/1/2
    ''')

if len(sys.argv) < 2:
    print_usage();
    exit(0)

module = sys.argv[1]
command = sys.argv[2] if len(sys.argv) > 2 else "main"

if (module not in ["net", "usereg", "user"]):
    print("no module: " + module)
    print_usage();
    exit(0)

m = __import__(module, globals(), locals(), level = 1)
try:
    getattr(m, command)(*sys.argv[3:])
except AttributeError:
    print('no method: ' + sys.argv[2])
