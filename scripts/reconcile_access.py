#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataSec Access Reconciliation

Назначение:
- сверить ожидаемые доступы из IDM;
- сверить фактическое членство пользователей в LDAP-группах;
- сверить наличие групп в политиках Apache Ranger;
- сформировать Markdown-отчет о расхождениях.

Скрипт работает с обезличенными CSV/JSON-файлами.
В production вместо файловых loader-ов можно подключить:
- IDM API;
- LDAP API / ldapsearch export;
- Apache Ranger REST API.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def read_expected_access(path: Path) -> set[tuple[str, str]]:
    """
    Читает ожидаемые доступы из IDM-выгрузки.

    Формат CSV:
    user,group,system,role,valid_to
    ivan.ivanov,dl_sales_orders_ro,trino,Sales Orders Read,2026-12-31
    """
    records: set[tuple[str, str]] = set()
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required_columns = {"user", "group"}
        missing_columns = required_columns - set(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(
                f"В файле {path} отсутствуют обязательные колонки: {sorted(missing_columns)}"
            )
        for row in reader:
            user = normalize(row.get("user"))
            group = normalize(row.get("group"))
            if user and group:
                records.add((user, group))
    return records


def read_ldap_memberships(path: Path) -> set[tuple[str, str]]:
    """
    Читает фактическое членство пользователей в LDAP-группах.

    Формат JSON:
    {
      "memberships": [
        {"user": "ivan.ivanov", "group": "dl_sales_orders_ro"}
      ]
    }
    """
    records: set[tuple[str, str]] = set()
    if not path.exists():
        return records
    data = read_json(path)
    for item in data.get("memberships", []):
        user = normalize(item.get("user"))
        group = normalize(item.get("group"))
        if user and group:
            records.add((user, group))
    return records


def read_ranger_policy_groups(path: Path) -> set[str]:
    """
    Читает группы, которые используются в политиках Ranger.

    Упрощенный формат JSON:
    {
      "policies": [
        {
          "name": "trino_sales_orders_select",
          "groups": ["dl_sales_orders_ro"]
        }
      ]
    }

    В production этот файл может формироваться из Apache Ranger REST API.
    """
    groups: set[str] = set()
    if not path.exists():
        return groups
    data = read_json(path)
    for policy in data.get("policies", []):
        for group in policy.get("groups", []):
            normalized_group = normalize(group)
            if normalized_group:
                groups.add(normalized_group)
    return groups


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в файле {path}: {error}") from error


def normalize(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def build_report(
    expected_access: set[tuple[str, str]],
    actual_ldap_memberships: set[tuple[str, str]],
    ranger_policy_groups: set[str],
) -> str:
    missing_in_ldap = expected_access - actual_ldap_memberships
    excessive_in_ldap = actual_ldap_memberships - expected_access

    expected_groups = {group for _, group in expected_access}
    ldap_groups = {group for _, group in actual_ldap_memberships}
    groups_without_ranger_policy = sorted((expected_groups | ldap_groups) - ranger_policy_groups)
    ranger_groups_without_idm_access = sorted(ranger_policy_groups - (expected_groups | ldap_groups))

    lines: list[str] = []
    lines.append("# Access Reconciliation Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Expected IDM memberships | {len(expected_access)} |")
    lines.append(f"| Actual LDAP memberships | {len(actual_ldap_memberships)} |")
    lines.append(f"| Ranger policy groups | {len(ranger_policy_groups)} |")
    lines.append(f"| Missing in LDAP | {len(missing_in_ldap)} |")
    lines.append(f"| Excessive in LDAP | {len(excessive_in_ldap)} |")
    lines.append(f"| Groups without Ranger policy | {len(groups_without_ranger_policy)} |")
    lines.append(f"| Ranger groups without IDM/LDAP access | {len(ranger_groups_without_idm_access)} |")
    lines.append("")
    lines.append("## 1. Missing in LDAP")
    lines.append("")
    lines.append(
        "Пользователь должен состоять в группе по данным IDM, но фактически не найден в LDAP-группе."
    )
    lines.append("")
    append_membership_table(lines, missing_in_ldap)
    lines.append("")
    lines.append("## 2. Excessive in LDAP")
    lines.append("")
    lines.append(
        "Пользователь фактически состоит в LDAP-группе, но такого доступа нет в IDM-выгрузке."
    )
    lines.append("")
    append_membership_table(lines, excessive_in_ldap)
    lines.append("")
    lines.append("## 3. Groups without Ranger policy")
    lines.append("")
    lines.append(
        "Группы есть в IDM/LDAP, но не найдены в политиках Ranger. "
        "Пользователь может быть добавлен в группу, но доступ в Trino не будет выдан."
    )
    lines.append("")
    append_group_list(lines, groups_without_ranger_policy)
    lines.append("")
    lines.append("## 4. Ranger groups without IDM/LDAP access")
    lines.append("")
    lines.append(
        "Группы используются в политиках Ranger, но не найдены в ожидаемых или фактических доступах. "
        "Это может быть устаревшая или ошибочная политика."
    )
    lines.append("")
    append_group_list(lines, ranger_groups_without_idm_access)
    lines.append("")
    lines.append("## Recommended actions")
    lines.append("")
    lines.append("1. Проверить все excessive-доступы и отозвать лишнее членство в LDAP.")
    lines.append("2. Проверить missing-доступы и понять, почему IDM-состояние не применилось в LDAP.")
    lines.append("3. Для групп без Ranger policy создать или скорректировать политики Ranger.")
    lines.append("4. Для Ranger-групп без IDM/LDAP-доступов проверить актуальность политик.")
    lines.append("5. После исправлений повторно запустить сверку.")
    lines.append("")
    return "\n".join(lines)


def append_membership_table(lines: list[str], rows: set[tuple[str, str]]) -> None:
    if not rows:
        lines.append("Расхождений не найдено.")
        return
    lines.append("| User | Group |")
    lines.append("|---|---|")
    for user, group in sorted(rows):
        lines.append(f"| `{user}` | `{group}` |")


def append_group_list(lines: list[str], groups: list[str]) -> None:
    if not groups:
        lines.append("Расхождений не найдено.")
        return
    for group in groups:
        lines.append(f"- `{group}`")


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare expected IDM access with LDAP memberships and Ranger policy groups."
    )
    parser.add_argument(
        "--expected",
        default="examples/idm_expected_access.csv",
        help="CSV-файл с ожидаемыми доступами из IDM.",
    )
    parser.add_argument(
        "--ldap",
        default="examples/ldap_actual_memberships.json",
        help="JSON-файл с фактическим членством в LDAP-группах.",
    )
    parser.add_argument(
        "--ranger",
        default="examples/ranger_policies.json",
        help="JSON-файл с группами, используемыми в политиках Ranger.",
    )
    parser.add_argument(
        "--report",
        default="reports/access-drift.md",
        help="Путь для Markdown-отчета.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    expected_access = read_expected_access(Path(args.expected))
    actual_ldap_memberships = read_ldap_memberships(Path(args.ldap))
    ranger_policy_groups = read_ranger_policy_groups(Path(args.ranger))

    report = build_report(
        expected_access=expected_access,
        actual_ldap_memberships=actual_ldap_memberships,
        ranger_policy_groups=ranger_policy_groups,
    )
    write_report(Path(args.report), report)

    missing = expected_access - actual_ldap_memberships
    excessive = actual_ldap_memberships - expected_access

    print(f"Expected IDM memberships: {len(expected_access)}")
    print(f"Actual LDAP memberships: {len(actual_ldap_memberships)}")
    print(f"Ranger policy groups: {len(ranger_policy_groups)}")
    print(f"Missing in LDAP: {len(missing)}")
    print(f"Excessive in LDAP: {len(excessive)}")
    print(f"Report: {args.report}")

    if missing or excessive:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
