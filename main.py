# Copyright © 2018 Stanislav Hnatiuk.  All rights reserved.

#!/usr/bin/env python3

import loader
import analyzer


def main():
    conn, cur = loader.connection()
    loader.get_struct(conn, cur)
    loader.get_dates(conn, cur)

    an = analyzer.Analyzer()
    # TODO: for dates
    loader.get_sfile(conn, cur, '2017-03-21')
    an.filtering()


if __name__ == "__main__":
    main()
