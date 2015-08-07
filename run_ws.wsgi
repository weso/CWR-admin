#!/usr/bin/python
import sys
import logging
from cwr_admin import create_app

sys.path.insert(0,"/var/www/cwr_admin/")
#os.chdir("/var/www/cwr_admin")

application = create_app()