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
  created_at: string;
}