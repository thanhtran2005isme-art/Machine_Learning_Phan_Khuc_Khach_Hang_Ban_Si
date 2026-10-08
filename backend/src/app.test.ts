import { describe, expect, it } from 'vitest';
import { buildApp } from './app.js';

const example = { Fresh: 6410.5, Milk: 7226, Grocery: 10842.5, Frozen: 1153, Detergents_Paper: 4084.5, Delicassen: 1508.5 };

describe('Gate 6: frozen serving', () => {
  it('loads frozen D011 model and exposes truthful health/model info', async () => {
    const app = buildApp();
    const health = await app.inject({ method: 'GET', url: '/api/health' });
    expect(health.statusCode).toBe(200);
    expect(health.json().modelReady).toBe(true);
    const response = await app.inject({ method: 'GET', url: '/api/model-info' });
    expect(response.statusCode).toBe(200);
    expect(response.json()).toMatchObject({ k: 2, preprocessing: 'log1p_standardscaler', training_count: 352 });
    await app.close();
  });
  it('predicts a real profile with centroid distance', async () => {
    const app = buildApp();
    const response = await app.inject({ method: 'POST', url: '/api/segment', payload: example });
    expect(response.statusCode).toBe(200);
    const body = response.json();
    expect([0, 1]).toContain(body.cluster_id);
    expect(body.distance_to_centroid).toBeGreaterThanOrEqual(0);
    expect(body.distances_to_centroids).toHaveLength(2);
    expect(body.profile.median_spending.Grocery).toBeGreaterThan(0);
    await app.close();
  });
  it.each([
    {}, { ...example, Fresh: -1 }, { ...example, Fresh: '123' },
    { ...example, extra: 1 }, { ...example, Fresh: null },
  ])('rejects malformed spending without coercion', async (payload) => {
    const app = buildApp();
    const response = await app.inject({ method: 'POST', url: '/api/segment', payload });
    expect(response.statusCode).toBe(400);
    expect(response.json().status).toBe('invalid_input');
    await app.close();
  });
  it('serves real experiment metrics and frozen evaluation without training', async () => {
    const app = buildApp();
    const response = await app.inject({ method: 'GET', url: '/api/dashboard' });
    expect(response.statusCode).toBe(200);
    expect(response.json().experiments).toHaveLength(14);
    expect(response.json().final_test.rows).toBe(88);
    await app.close();
  });
  it('fails closed when the model is absent or corrupt', async () => {
    const app = buildApp({ modelPath: '/path/that/does/not/exist.json' });
    expect((await app.inject({ method: 'GET', url: '/api/health' })).json().modelReady).toBe(false);
    expect((await app.inject({ method: 'POST', url: '/api/segment', payload: example })).statusCode).toBe(503);
    expect((await app.inject({ method: 'GET', url: '/api/model-info' })).statusCode).toBe(503);
    await app.close();
  });
});
