#!/usr/bin/env python

USERNAME = 'alejandra'
PASSWORD = 'proton022'
SERVER = 'http://codenga.com/reviews/'
LOGIN_OPTIONS = '--username={0} --password={1} --server={2}'.format(USERNAME, PASSWORD, SERVER)
OPTIONS = '{0} --guess-description -o --target-groups=Tech'.format(LOGIN_OPTIONS)

import re
import sys
from subprocess import call, Popen, PIPE

def get_branch():
    p = Popen("git symbolic-ref HEAD 2>/dev/null | sed -e 's|^refs/heads/||'", shell=True, stdout=PIPE)
    branch = p.communicate()[0].strip()
    return branch

def get_issue_number(branch):
    issue_re = re.compile(r'.+/.+/(?P<issue_number>\d+)-.+')
    match = issue_re.match(branch)
    return match.group('issue_number')

def get_review_to_update():
    try:
        u = sys.argv[1]
        if u:
            return '-r {0}'.format(u)
        return ''
    except IndexError:
        return ''

def main():
    branch = get_branch()
    review_to_update = get_review_to_update()
    issue_number = get_issue_number(branch)
    command = ('post-review {0} '
               ' --branch="{1}" --summary="{1}" --bugs-closed="{2}"'
               ' --revision-range=master:"{1}" {3}'
               .format(OPTIONS, branch, issue_number, review_to_update))
    #print command
    call(command, shell=True)

if __name__ == "__main__":
    main()
