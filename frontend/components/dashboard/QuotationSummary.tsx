interface Props {
  quotation: {
    base_cost: number;
    sample_cost: number;
    programming_fee: number;
    translation_fee: number;
    pm_fee: number;
    margin: number;
    rush_fee: number;
    client_discount: number;
    total_cost: number;
    currency: string;
  };
}

export default function QuotationSummary({
  quotation,
}: Props) {
  function money(value: number) {
    return `${quotation.currency} ${value.toLocaleString("en-US")}`;
  }

  return (
    <section className="detail-card">
      <h2>Quotation Summary</h2>

      <div className="info-row">
        <span>Base Cost</span>
        <strong>{money(quotation.base_cost)}</strong>
      </div>

      <div className="info-row">
        <span>Sample Cost</span>
        <strong>{money(quotation.sample_cost)}</strong>
      </div>

      <div className="info-row">
        <span>Programming</span>
        <strong>{money(quotation.programming_fee)}</strong>
      </div>

      <div className="info-row">
        <span>Translation</span>
        <strong>{money(quotation.translation_fee)}</strong>
      </div>

      <div className="info-row">
        <span>PM Fee</span>
        <strong>{money(quotation.pm_fee)}</strong>
      </div>

      <div className="info-row">
        <span>Margin</span>
        <strong>{money(quotation.margin)}</strong>
      </div>

      <div className="info-row">
        <span>Rush Fee</span>
        <strong>{money(quotation.rush_fee)}</strong>
      </div>

      <div className="info-row">
        <span>Client Discount</span>
        <strong>{money(quotation.client_discount)}</strong>
      </div>

      <div className="quotation-total">
        <span>Total</span>

        <strong>
          {money(quotation.total_cost)}
        </strong>
      </div>
    </section>
  );
}