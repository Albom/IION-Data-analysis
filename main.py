# Copyright © 2018 Stanislav Hnatiuk.  All rights reserved.

#!/usr/bin/env python3

import loader
import json


def main():
    conn, cur = loader.connection()
    loader.get_struct(conn, cur)
    loader.get_dates(conn, cur)
    loader.get_sfile(conn, cur, '2017-03-21')


if __name__ == "__main__":
    main()
