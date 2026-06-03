export declare class FireAntClient {
  private request;
  get(path: string, query?: Record<string, string | number | undefined>): Promise<unknown>;
  post(path: string, body?: unknown): Promise<unknown>;
}
