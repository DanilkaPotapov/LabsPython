from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass(frozen=True)
class StudentGroup:
    id: int
    name: str
    size: int
    department_id: int

@dataclass(frozen=True)
class Department:
    id: int
    name: str

@dataclass(frozen=True)
class GroupDepartment:
    group_id: int
    department_id: int

def build_sample_data() -> tuple[List[Department], list[StudentGroup], list[GroupDepartment]]:
    departments = [
        Department(1, "Кафедра прикладной математики"),
        Department(2, "Кафедра программной инженерии"),
        Department(3, "Кафедра информационной безопасности"),
    ]

    groups = [
        StudentGroup(1, "A-101", 28, 2),
        StudentGroup(2, "Б-202", 22, 1),
        StudentGroup(3, "A-103", 30, 2),  # Латинская A
        StudentGroup(4, "В-305", 19, 3),
        StudentGroup(5, "Г-404", 25, 1),
    ]

    links = [
        GroupDepartment(1, 2),
        GroupDepartment(1, 3),
        GroupDepartment(2, 1),
        GroupDepartment(3, 2),
        GroupDepartment(3, 1),
        GroupDepartment(4, 3),
        GroupDepartment(5, 1),
        GroupDepartment(5, 2),
    ]

    return departments, groups, links

def _dept_by_id(departments: list[Department]) -> dict[int, Department]:
    return {d.id: d for d in departments}

def _group_by_id(groups: list[StudentGroup]) -> dict[int, StudentGroup]:
    return {g.id: g for g in groups}

def query1_groups_starting_with_a(groups: list[StudentGroup], departments: list[Department]) -> list[tuple]:
    dept = _dept_by_id(departments)
    return [(g.name, dept[g.department_id].name) for g in groups if g.name.startswith("A")]

def query2_departments_with_min_group_size(groups: list[StudentGroup], departments: list[Department]) -> list[tuple]:
    dept = _dept_by_id(departments)
    sizes_by_dept: dict[int, list[int]] = {}
    for g in groups:
        sizes_by_dept.setdefault(g.department_id, []).append(g.size)

    mins = sorted(((dept_id, min(sizes)) for dept_id, sizes in sizes_by_dept.items()), key=lambda x: x[1])
    return [(dept[dept_id].name, min_size) for dept_id, min_size in mins]

def query3_group_department_links(
    groups: list[StudentGroup],
    departments: list[Department],
    links: list[GroupDepartment],
) -> list[tuple[str, str]]:
    dept = _dept_by_id(departments)
    grp = _group_by_id(groups)
    return sorted(
        ((grp[link.group_id].name, dept[link.department_id].name) for link in links),
        key=lambda x: x[0]
    )

def run_demo() -> str:
    departments, groups, links = build_sample_data()
    out: list[str] = []

    q1 = query1_groups_starting_with_a(groups, departments)
    out.append("Запрос 1. Группы, начинающиеся на 'А', и их кафедры (1:N):")
    for group_name, dept_name in q1:
        out.append(f"  {group_name} - {dept_name}")
    out.append("")

    q2 = query2_departments_with_min_group_size(groups, departments)
    out.append("Запрос 2. Кафедры и минимальная численность группы на кафедре (1:N), сортировка по минимуму:")
    for dept_name, min_size in q2:
        out.append(f"  {dept_name}: минимум = {min_size}")
    out.append("")

    q3 = query3_group_department_links(groups, departments, links)
    out.append("Запрос 3. Связанные группы и кафедры (М:N), сортировка по группам:")
    for group_name, dept_name in q3:
        out.append(f"  {group_name} - {dept_name}")
    return "\n".join(out)

if __name__ == "__main__":
    print(run_demo())