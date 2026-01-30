import json
from typing import Any

class FileHandler:
    @staticmethod
    def write_file(data: list[dict[Any, Any]], output_file_path: str) -> None:
        try:
            with open(output_file_path, 'w', encoding='cp1250') as file:
                json.dump(data, file, indent=2)
            print('File written to ' + output_file_path)
        except IOError as e:
            raise IOError(e)