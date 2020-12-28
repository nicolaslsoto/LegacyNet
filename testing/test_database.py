import unittest

from database import Database


class TestDatabase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDatabase, self).__init__(*args, **kwargs)
        self.database = Database("unittest.db")

    def test_table(self):
        self.database.create_table("test_table")
        self.assertListEqual(self.database.get_tables(), ["test_table"], "Should be [test_table]")
        self.database.add_entry("test_table", 1, 2, 3, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0)
        df = self.database.get_gravestones("test_table")
        self.assertEqual(len(df.index), 1, "df rows should be 1")
        row = df.iloc[0]
        self.assertEqual((row["id"], row["row"], row["col"],
                          row["toplx"], row["toply"], row["toprx"], row["topry"],
                          row["botlx"], row["botly"], row["botrx"], row["botry"],
                          row["centroidx"], row["centroidy"]),
                         (1, 2, 3,
                          4.0, 5.0, 6.0, 7.0,
                          8.0, 9.0, 10.0, 11.0,
                          12.0, 13.0)
                         )
        self.database.delete_table("test_table")
        self.assertListEqual(self.database.get_tables(), [], "Should be empty")


if __name__ == '__main__':
    unittest.main()
