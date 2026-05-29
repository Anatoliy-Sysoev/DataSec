# Скрипты

Каталог содержит утилиты для проверки и сопровождения DataSec-решения.

## Скрипты

- `reconcile_access.py` — сверка ожидаемых доступов из IDM с фактическим членством в LDAP-группах и группами в политиках Ranger.
- `render_diagrams.sh` — рендер PlantUML и Mermaid-диаграмм в PNG/SVG.

## reconcile_access.py

Сверяет три источника и формирует Markdown-отчет о расхождениях:

```text
IDM expected access  vs  LDAP actual memberships  vs  Ranger policy groups
```

Запуск с обезличенными примерами из `examples/`:

```bash
python3 scripts/reconcile_access.py
```

Параметры (по умолчанию указывают на файлы в `examples/`):

| Флаг | Назначение |
|---|---|
| `--expected` | CSV с ожидаемыми доступами из IDM |
| `--ldap` | JSON с фактическим членством в LDAP-группах |
| `--ranger` | JSON с группами, используемыми в политиках Ranger |
| `--report` | Путь для Markdown-отчета (по умолчанию `reports/access-drift.md`) |

Коды возврата: `0` — расхождений нет; `2` — найдены missing/excessive доступы.
В production файловые loader-ы заменяются на IDM API, LDAP export и Apache Ranger REST API.

## Принцип

Скрипты должны работать от обезличенных CSV/JSON-выгрузок и не содержать внутренних адресов, токенов или учетных данных.
