import re
from typing import List, Dict, Any

class DrillParser:
    """
    Simulates the 'Drill Result Interpreter' by parsing text for geological intervals and grades.
    """

    def __init__(self):
        # Regex for number that allows integers, floats, and .5 style
        number_re = r"(?:\d+(?:\.\d*)?|\.\d+)"

        # Pattern 1: [Interval] [Unit] @ [Grade] [GradeUnit] [Element]
        # Example: "10.5m @ 3.4 g/t Au"
        self.pattern1 = re.compile(
            rf"({number_re})\s*(m|meters|ft|feet)\s*(?:@|at|of)\s*({number_re})\s*(g/t|%|ppm)\s*([A-Za-z]+)",
            re.IGNORECASE
        )

        # Pattern 2: [Grade] [GradeUnit] [Element] (over/across) [Interval] [Unit]
        # Example: "3.4 g/t Au over 10.5m"
        self.pattern2 = re.compile(
            rf"({number_re})\s*(g/t|%|ppm)\s*([A-Za-z]+)\s*(?:over|across)\s*({number_re})\s*(m|meters|ft|feet)",
            re.IGNORECASE
        )

    def parse_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse a text string and extract drill highlights.
        """
        results = []

        # Process Pattern 1
        matches1 = self.pattern1.findall(text)
        for match in matches1:
            # match returns (interval, unit, grade, grade_unit, element)
            # But wait, number_re has groups? No, (?:...) is non-capturing.
            # However, I used rf"({number_re})..." so the whole number_re is group 1.
            # Let's verify groups.
            # r"((?:\d+(?:\.\d*)?|\.\d+))\s*(m|...)..."
            # Groups: 1=Interval, 2=Unit, 3=Grade, 4=GradeUnit, 5=Element
            interval, unit, grade, grade_unit, element = match
            results.append(self._format_result(float(interval), unit, float(grade), grade_unit, element))

        # Process Pattern 2
        matches2 = self.pattern2.findall(text)
        for match in matches2:
            grade, grade_unit, element, interval, unit = match
            results.append(self._format_result(float(interval), unit, float(grade), grade_unit, element))

        return results

    def _format_result(self, interval, unit, grade, grade_unit, element):
        normalized_interval = self._normalize_length(interval, unit)
        return {
            "raw_interval": interval,
            "raw_unit": unit,
            "raw_grade": grade,
            "grade_unit": grade_unit,
            "element": element,
            "normalized_interval_m": normalized_interval,
            "formatted": f"{interval}{unit} @ {grade} {grade_unit} {element}"
        }

    def _normalize_length(self, value: float, unit: str) -> float:
        """Convert feet to meters."""
        unit = unit.lower()
        if unit in ['ft', 'feet']:
            return round(value * 0.3048, 2)
        return value

    def calculate_metal_content(self, intercepts: List[Dict[str, Any]], target_element: str = "Au") -> float:
        """
        Calculate 'Gram-Meters' for a specific element.
        """
        score = 0.0
        target = target_element.lower()
        for i in intercepts:
            # Check element match (simple check)
            if i['element'].lower() == target and i['grade_unit'] == 'g/t':
                score += i['normalized_interval_m'] * i['raw_grade']
        return round(score, 2)
