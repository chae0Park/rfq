from typing import List


class ClarificationGenerator:
    """
    Generates clarification questions for missing RFQ information.
    """

    QUESTION_MAP = {
        "country": "Which country will the survey be conducted in?",
        "sample_size": "What is the required sample size?",
        "target_audience": "Who is the target audience?",
        "timeline": "What is the project timeline?",
        "methodology": "Which research methodology should be used?",
        "quota": "Are there any quota requirements?",
        "translation_required": "Is translation required?",
        "programming_required": "Is survey programming required?",
        "overlay_required": "Is data overlay required?",
        "project_scope": "Is this a Full Service project or Fieldwork Only?",
        "loi": "What is the expected Length of Interview (LOI)?",
        "ir": "What is the expected Incidence Rate (IR)?",
        "panel_cpi": "What is the Panel CPI?",
        "base_cost": "What is the Country Base Cost?",
        "margin": "What margin should be applied?",
    }

    def generate(self, missing_fields: List[str]) -> List[str]:
        return [
            self.QUESTION_MAP[field]
            for field in missing_fields
            if field in self.QUESTION_MAP
        ]