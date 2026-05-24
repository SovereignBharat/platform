export class SovereignBharatClient {
  constructor(private apiUrl: string) {}

  async health() {
    const response = await fetch(`${this.apiUrl}/health`)
    return response.json()
  }
}
