export interface LLMCallLog {
  id: number;
  rfq_id: number | null;
  task_type: string;
  model: string;
  status: string;

  latency_ms: number | null;
  input_tokens: number | null;
  output_tokens: number | null;
  estimated_cost: number | null;
  error_message: string | null;
}

export interface LLMMonitoringSummary {
  total_calls: number;
  successful_calls: number;
  failed_calls: number;
  success_rate: number;

  total_input_tokens: number;
  total_output_tokens: number;
  total_tokens: number;

  average_latency_ms: number;
  total_estimated_cost: number;
}