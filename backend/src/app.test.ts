import { describe, expect, it } from 'vitest';

import { buildApp } from './app.js';

describe('API skeleton', () => {
  it('GET /api/health returns service status without pretending model is ready', async () => {
    const app = buildApp();
    const response = await app.inject({ method: 'GET', url: '/api/health' });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({
      status: 'ok',
      service: 'wholesale-customer-segmentation-api',
      modelReady: false,
    });

    await app.close();
  });

  it('GET /api/model-info stays unavailable before ML model is frozen', async () => {
    const app = buildApp();
    const response = await app.inject({ method: 'GET', url: '/api/model-info' });

    expect(response.statusCode).toBe(503);
    expect(response.json().status).toBe('not_ready');

    await app.close();
  });
});
