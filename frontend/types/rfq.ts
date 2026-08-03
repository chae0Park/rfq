export interface QuotationSummary {
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
}

export interface RFQ {
  id: number;
  client_name: string | null;
  client_email: string | null;
  client: string | null;
  project_name: string | null;
  country: string | null;
  sample_size: number | null;
  timeline: string | null;
  methodology: string | null;
  status: string;
  created_at?: string;
  total_cost: number | null;
  currency: string | null;
  quotation: QuotationSummary | null;
}