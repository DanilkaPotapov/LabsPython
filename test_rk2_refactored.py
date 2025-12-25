import unittest
import rk2_refactored as rk

class TestQueries(unittest.TestCase):
    def setUp(self):
        self.departments, self.groups, self.links = rk.build_sample_data()

    def test_query1_groups_starting_with_a(self):
        result = rk.query1_groups_starting_with_a(self.groups, self.departments)
        expected = [
            ("A-101", "Кафедра программной инженерии"),
            ("A-103", "Кафедра программной инженерии"),
        ]
        self.assertEqual(result, expected)

    def test_query2_departments_with_min_group_size_sorted(self):
        result = rk.query2_departments_with_min_group_size(self.groups, self.departments)
        expected = [
            ("Кафедра информационной безопасности", 19),
            ("Кафедра прикладной математики", 22),
            ("Кафедра программной инженерии", 28),
        ]
        self.assertEqual(result, expected)

    def test_query3_links_sorted_by_group(self):
        result = rk.query3_group_department_links(self.groups, self.departments, self.links)
        
        self.assertEqual(len(result), len(self.links))
        
        self.assertEqual(result[0][0], "A-101")

        a101_depts = [dept for grp, dept in result if grp == "A-101"]
        expected_a101_depts = {"Кафедра программной инженерии", "Кафедра информационной безопасности"}
        self.assertEqual(set(a101_depts), expected_a101_depts)
        
        link_groups = {rk._group_by_id(self.groups)[link.group_id].name for link in self.links}
        result_groups = {grp for grp, _ in result}
        self.assertEqual(link_groups, result_groups)

if __name__ == "__main__":
    unittest.main(verbosity=2)
