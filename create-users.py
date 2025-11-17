#!/usr/bin/python3

# INET4031 - Automated User Creation Script
# Author: Feysal Ali
# Description:
# This script reads a list of users from stdin and automates creation
# of user accounts, password assignment, and group memberships.

import os
import sys
import re

def main():

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        if re.match(r"^#", line):
            continue

        fields = line.split(":")

        if len(fields) < 5:
            continue

        username, password, last_name, first_name, groups = fields
        gecos = f"{first_name} {last_name},,,"
        group_list = groups.split(",")

        # Create user
        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        os.system(cmd)

        # Set password
        print(f"==> Setting the password for {username}...")
        cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        os.system(cmd)

        # Add groups
        for group in group_list:
            if group != '-' and group.strip():
                print(f"==> Assigning {username} to the {group} group...")
                cmd = f"/usr/sbin/adduser {username} {group}"
                os.system(cmd)

if __name__ == "__main__":
    main()
