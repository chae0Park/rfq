from app.models.request import RFQRequest
from app.services.rfq_service import RFQService
from app.config.database import SessionLocal


def main():
    db = SessionLocal()
    service = RFQService(db)

    request = RFQRequest(
        email="""
Hi Team,

We have a new online research project.

Project Name: Smartphone Usage Study 2026

Country: South Korea

Sample Size: 1000 completes

Target Audience:
Adults aged 18-55

Gender:
All genders

Timeline:
Fieldwork should start next Monday and finish within one week.

Methodology:
Online Survey

Translation:
English to Korean translation required.

Programming:
Programming required.

Overlay:
No overlay required.

This is a full-service project.

Best regards,
John
"""
    )

    result = service.process_email(request)

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()