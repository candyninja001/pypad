class JsonParser:
    def __init__(self):
        self._report_list = []
        self._report_dev_list = []

    def _report(self, message: str):
        self._report_list.append(message)

    def _report_dev(self, message: str):
        self._report_dev_list.append(message)

    def _clear_reports(self):
        self._report_list = []
        self._report_dev_list = []
    
    def get_tag(self) -> str:
        return self.__class__.__name__

    def get_reports(self) -> [str]:
        return self._report_list

    def get_reports_dev(self) -> [str]:
        return self._report_dev_list

    def parsable(self, raw_data: dict) -> bool:
        return False

    def parse(self, raw_data: dict) -> dict:
        return {}
