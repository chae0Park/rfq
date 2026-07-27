from app.models.rfq import RFQExtraction
from app.services.calculator import RFQCalculator


def main():
    
    rfq = RFQExtraction(
        countries=[
            "South Korea",
            "Japan",
        ],
        sample_size=500,
        loi=15,
        ir=30,
        languages=[
            "Korean",
            "Japanese"
        ],
        currency="EUR",
    )
    calculator = RFQCalculator()

    result = calculator.calculate(rfq)

    print(result.model_dump())


if __name__ == "__main__":
    main()