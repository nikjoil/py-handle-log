from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Dict, Any, Tuple, Optional


class GenReport(ABC):
    @abstractmethod
    def process_log(self, logs: List[Dict[str, Any]]) -> Any:
        pass

    @abstractmethod
    def render_report(self, processed_data: Any, report_date: Optional[str] = None) -> Tuple[str, List[List[Any]], List[str]]:
        pass


class AverageTimeReport(GenReport):
    def process_log(self, logs: List[Dict[str, Any]]):
        endpoints = defaultdict(lambda: {"count": 0, "total_time": 0.0})
        for entry in logs:
            url = entry.get("url")
            rt = entry.get("response_time")
            if url and isinstance(rt, (int, float)):
                endpoints[url]["count"] += 1
                endpoints[url]["total_time"] += rt
        return endpoints

    def render_report(self, processed_data, report_date: Optional[str] = None):
        rows = []
        for endpoint, v in processed_data.items():
            if v["count"]:
                avg = v["total_time"] / v["count"]
                rows.append([endpoint, v["count"], round(avg, 3)])
        headers = ["handler", "total", "avg_response_time"]
        title = "Отчет c количеством запросов и средним временем ответа"
        if report_date:
            title += f" за {report_date}"
        return title, rows, headers


class UserAgentRep(GenReport):
    def process_log(self, logs: List[Dict[str, Any]]):
        counts = defaultdict(int)
        for entry in logs:
            ua = entry.get("http_user_agent")
            if ua and ua != "...":
                if "Chrome/" in ua and "Safari/" in ua:
                    counts["Chrome"] += 1
                elif "Firefox/" in ua:
                    counts["Firefox"] += 1
                elif "Safari/" in ua:
                    counts["Safari"] += 1
                else:
                    counts["Other"] += 1
        return counts

    def render_report(self, processed_data, report_date: Optional[str] = None):
        rows = list(processed_data.items())
        headers = ["User-Agent", "total"]
        title = "Отчет по браузерам"
        if report_date:
            title += f" за {report_date}"
        return title, rows, headers


REPORT = {"average": AverageTimeReport, "user_agent": UserAgentRep}
