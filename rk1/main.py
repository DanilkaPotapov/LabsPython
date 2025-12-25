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

def main() -> None:
    departments: List[Department] = [
        Department(1, "Кафедра прикладной математики"),
        Department(2, "Кафедра программной инженерии"),
        Department(3, "Кафедра информационной безопасности"),
    ]
    groups: List[StudentGroup] = [
        StudentGroup(1, "A-101", 28, 2),
        StudentGroup(2, "B-202", 22, 1),
        StudentGroup(3, "A-103", 30, 2),
        StudentGroup(4, "B-305", 19, 3),
        StudentGroup(5, "Г-404", 25, 1),
    ]
    group_departments: List[GroupDepartment] = [
        GroupDepartment(1, 2),
        GroupDepartment(1, 3),
        GroupDepartment(2, 1),
        GroupDepartment(5, 2),
        GroupDepartment(3, 1),
        GroupDepartment(4, 3),
        GroupDepartment(5, 1),
        GroupDepartment(5, 2),
    ]
    dept_by_id: Dict[int, Department] = {d.id: d for d in departments}
    group_by_id: Dict[int, StudentGroup] = {g.id: g for g in groups}

    q1: List[Tuple[str, str]] = [
        (g.name, dept_by_id[g.department_id].name)
        for g in groups
        if g.name.startswith("A")
    ]
    print("Запрос 1. Группы, начинающиеся на 'А', и их кафедры (1:N):")
    for group_name, dept_name in q1:
        print(f"   {group_name} - {dept_name}")
    print()

    sizes_by_dept: Dict[int, List[int]] = {}
    for g in groups:
        sizes_by_dept.setdefault(g.department_id, []).append(g.size)

    q2: List[Tuple[str, int]] = sorted(
        [(dept_by_id[dept_id].name, min(sizes)) for dept_id, sizes in sizes_by_dept.items()],
        key=lambda x: x[1]
    )
    print("Запрос 2. Кафедры и минимальная численность группы на кафедре (1:N), сортировка по минимуму:")
    for dept_name, min_size in q2:
        print(f"   {dept_name}: минимум = {min_size}")
    print()

    q3: List[Tuple[str, str]] = sorted(
        [(group_by_id[gd.group_id].name, dept_by_id[gd.department_id].name) for gd in group_departments],
        key=lambda x: x[0]
    )
    print("Запрос 3. Связанные группы и кафедры (M:N), сортировка по группам:")
    for group_name, dept_name in q3:
        print(f"   {group_name} - {dept_name}")

if __name__ == "__main__":
    main()
