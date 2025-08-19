from tabulate import tabulate
from handle_log.parser import parse_arg
from handle_log.log_io import read_logs, filter_data_logs
from handle_log.reports import REPORT, AverageTimeReport, UserAgentRep


def main() -> None:
    args = parse_arg()
    logs = read_logs(args.file)
    filtered = filter_data_logs(logs, args.date)

    if not filtered:
        print(f"Нет логов для даты: {args.date}")
        return

    report_cls = REPORT.get(args.report)
    if not report_cls:
        print(f"Ошибка: отчет '{args.report}' не найден")
        return

    report_gen = report_cls()
    processed = report_gen.process_log(filtered)
    title, table_data, headers = report_gen.render_report(
        processed, report_date=args.date
    )

    print(f"\n{title}\n")
    print(tabulate(table_data, headers=headers))


if __name__ == "__main__":
    main()


# Экспортируем имена, которые используют тесты
__all__ = ["AverageTimeReport", "UserAgentRep", "filter_data_logs", "read_logs", "main"]
