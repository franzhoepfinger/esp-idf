#!/usr/bin/env python
#
# SPDX-FileCopyrightText: 2017-2024 Espressif Systems (Shanghai) CO LTD
#
# SPDX-License-Identifier: Apache-2.0
#
import argparse
import os
import subprocess
import sys

if __name__ == '__main__':
    # Here the argparse is used only to "peek" into arguments if
    # legacy version is requested or if old json format is specified.
    # In these two cases the esp_idf_size legacy version is spawned.
    parser = argparse.ArgumentParser(exit_on_error=False, add_help=False)
    parser.add_argument('--format')
    parser.add_argument('-l', '--legacy', action='store_true', default=os.environ.get('ESP_IDF_SIZE_LEGACY', '0') == '1')

    # The sys.argv is parsed with "exit_on_error", but the argparse.ArgumentError
    # exception should never occur, because unknown args should be put into
    # the rest variable, since the parse_known_args() method is used.
    args, rest = parser.parse_known_args()

    if not args.legacy and args.format != 'json':
        # By default start the refactored version, unless legacy version is explicitly requested with
        # -l/--legacy option or if old json format is specified.
        try:
            import esp_idf_size.ng  # noqa: F401
        except ImportError:
            print('warning: refactored esp-idf-size not installed, using legacy mode', file=sys.stderr)
            args.legacy = True
        else:
            os.environ['ESP_IDF_SIZE_NG'] = '1'
            if not rest or '-h' in rest or '--help' in rest:
                print(('Note: legacy esp_idf_size version can be invoked by specifying the -l/--legacy '
                       'option or by setting the ESP_IDF_SIZE_LEGACY environment variable.'))

    if args.format is not None:
        rest = ['--format', args.format] + rest

    sys.exit(subprocess.run([sys.executable, '-m', 'esp_idf_size'] + rest).returncode)
