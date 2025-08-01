import sys
import pytest
from main import (
    AverageTimeReport,
    UserAgentRep,
    filter_data_logs,
    read_logs,
    main,
)


def  test_average_time_report():
    logs = [
        {"url": "/api/users", "response_time": 0.2},
        {"url": "/api/data", "response_time": 0.5},
        {"url": "/api/users", "response_time": 0.4},
        {"url": "/api/users", "response_time": "slow"},
        {"url": "/api/data"},
    ]

    report = AverageTimeReport()
    res = report.process_log(logs)
    assert res['/api/users']['count'] == 2
    assert res['/api/users']['total_time'] == pytest.approx(0.6) # pytest.approx для точного сравнения float
    assert res['/api/data']['count'] == 1
    assert res['/api/data']['total_time'] == pytest.approx(0.5)
    

def test_user_agent_rep():
    logs = [
        {"http_user_agent": "Mozilla/5.0... Firefox/99.0"},
        {"http_user_agent": "Mozilla/5.0... Chrome/101.0... Safari/537.36"},
        {"http_user_agent": "Mozilla/5.0... Chrome/101.0... Safari/537.36"},
        {"http_user_agent": "Mozilla/5.0... Safari/605.1.15"},
        {"http_user_agent": "curl/7.68.0"},
        {"http_user_agent": "..."},         
        {"url": "/api/data"},               
    ]
    
    report = UserAgentRep()
    res = report.process_log(logs)
    assert res["Firefox"] == 1
    assert res["Chrome"] == 2
    assert res["Safari"] == 1
    assert res["Other"] == 1


def test_filter_data_logs():
    logs = [
        {"@timestamp": "2025-06-22T10:00:00+00:00"},
        {"@timestamp": "2025-06-22T23:59:59+00:00"},
        {"@timestamp": "2025-06-23T00:00:00+00:00"},
        {"@timestamp": "неверная_дата"},
        {},
    ]

    res_filter_date = filter_data_logs(logs, "2025-06-22")
    assert len(res_filter_date) == 2
    assert len(filter_data_logs(logs, None)) == 5


def test_read_logs(tmp_path):
    test_log = tmp_path / "test_read_logs.log"
    test_log.write_text('{"url": "/test_read_logs"}\n')

    broken_log = tmp_path / "broken.log"
    broken_log.write_text('{"url": /bad_json}')

    logs = read_logs([str(test_log), str(broken_log), "nonexist.log"])
    assert len(logs) == 1
    assert logs[0]['url'] == '/test_read_logs'


def test_main_integration_average_time_report(tmp_path, capsys):
    log_file = tmp_path / "test_integration.log"
    log_file.write_text(
        '{"@timestamp": "2025-10-25T10:00:00+00:00", "url": "/api/today", "response_time": 0.5}\n'
        '{"@timestamp": "2025-10-26T11:00:00+00:00", "url": "/api/tomorrow", "response_time": 0.1}\n'
    )

    sys.argv = ['main.py', '--file', str(log_file), '--report', 'average', '--date', '2025-10-25']
    main()
    captured = capsys.readouterr()
    console_output = captured.out

    assert "Отчет c количеством запросов и средним временем ответа за 2025-10-25" in console_output
    assert "/api/today" in console_output
    assert "/api/tomorrow" not in console_output