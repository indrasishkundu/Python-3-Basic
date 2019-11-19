#!python3
#pw.py-insecure password locker program
PASSWORDS={'email':'pakistankimaakabhoss',
            'blog':'tomatochahiyekya78',
            'luggage':'humaapkehainkaun69'}           #storing info

import sys,pyperclip
if len(sys.argv)<2:
    print('usage:python pw.py[account] - copy account password')
    sys.exit()
account=sys.argv[1]
if account in PASSWORDS:
    pyperclip.copy(PASSWORDS[account])
    print('Password for '+account+' copied to clipboard.')
else:
    print('there is no account named '+account)                  