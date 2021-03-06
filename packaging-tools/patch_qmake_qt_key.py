#!/usr/bin/env python
#############################################################################
##
## Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
## Contact: http://www.qt-project.org/legal
##
## This file is part of the release tools of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Digia.  For licensing terms and
## conditions see http://qt.digia.com/licensing.  For further information
## use the contact form at http://qt.digia.com/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 2.1 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU Lesser General Public License version 2.1 requirements
## will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Digia gives you certain additional
## rights.  These rights are described in the Digia Qt LGPL Exception
## version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
##
## $QT_END_LICENSE$
##
#############################################################################

"""Scripts to patch keys inside qmake executable"""

import os
import sys
import re


##############################################################
# Function
##############################################################
def replace_key(qmake_file_name, key, new_value):
    if not os.path.exists(qmake_file_name):
        print '*** Unable to open file: ' + qmake_file_name
        return False
    if not key:
        print '*** Given key empty! '
        return False
    if not new_value:
        print '*** Given new_value empty! '
        return False
    if len(new_value) > 255:
        print '*** Given new_value can not be longer than 255 or the binary would get corrupted! '
        print '*** Length for the given new value was: ' + str(len(new_value))
        return False

    filename = open(qmake_file_name, 'r+b')
    text = ''
    while True:
        temp = filename.read()
        if not temp or len(temp) == 0:
            break
        text = text + temp
    mkey = re.search(key + '=', text)
    if not mkey:
        print '*** Given key not found: ' + key
        print '*** Abort!'
        return False
    end_index = mkey.end()
    read_reamaining_offset = end_index + len(new_value) + 1
    replacement_text = text[0:end_index] + new_value + '\0' + text[read_reamaining_offset:]

    filename.seek(0)
    filename.write(replacement_text)
    filename.truncate()
    filename.close()
    return


##############################################################
# Function
##############################################################
def fetch_key(qmake_file_name, key):
    if not os.path.exists(qmake_file_name):
        print '*** Unable to open file: ' + qmake_file_name
        return False
    if not key:
        print '*** Given key empty! '
        return False

    filename = open(qmake_file_name, 'rb')
    text = ''
    while True:
        temp = filename.read()
        if not temp or len(temp) == 0:
            break
        text = text + temp
        print 'got text'

    filename.close()

    mkey = re.search(key + '=', text)
    if not mkey:
        print '*** Could not find given key: ' + key
        print '*** From: ' + qmake_file_name
        return ''
    end_index = mkey.end()

    text = text[end_index:]
    end_index_2 = re.search('\0', text)
    value = text[0:end_index_2.end() - 1]
    return value


##############################################################
# Function
##############################################################
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise RuntimeError('*** Three parameters needed!')
    print fetch_key(sys.argv[1], sys.argv[2])
    replace_key(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0)

