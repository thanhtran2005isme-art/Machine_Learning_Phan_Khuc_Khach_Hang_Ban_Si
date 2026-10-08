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
  it('never exposes filesystem paths in error responses for a missing model', async () => {
    const app=buildApp({modelPath:'C:\\\\private\\\\internal\\\\secret-model.json'});
    const response=await app.inject({method:'GET',url:'/api/model-info'});
    expect(response.statusCode).toBe(503);
    const error=response.json();
    expect(error.status).toBe('not_ready');
    expect(error.detail).toBeUndefined();
    expect(JSON.stringify(error)).not.toMatch(/private|internal|secret-model|ENOENT/i);
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

describe('Gate 9.3: validated final 352-development dashboard API', () => {
  it('keeps old dashboard fields and adds verified final profiles for six features', async () => {
    const app=buildApp();
    const response=await app.inject({method:'GET',url:'/api/dashboard'});
    expect(response.statusCode).toBe(200);
    const data=response.json();
    expect(data.experiments).toHaveLength(14);
    expect(data.training.rows).toBe(352);
    expect(data.final_test.rows).toBe(88);
    expect(data.profiles).toHaveLength(2);
    expect(data.final_profile).toMatchObject({
      source_scope:'train_plus_validation',development_count:352,read_only:true,test_used:false,
    });
    expect(data.final_profile.cluster_sizes.map((r:{count:number})=>r.count)).toEqual([162,190]);
    expect(data.final_profile.channel_profile.reduce((n:number,r:{count:number})=>n+r.count,0)).toBe(352);
    expect(data.final_profile.region_profile.reduce((n:number,r:{count:number})=>n+r.count,0)).toBe(352);
    expect(data.final_profile.distance_summary).toHaveLength(2);
    expect(data.final_profile.median_ratio).toHaveLength(2);
    await app.close();
  });
  it('returns 503 for missing Gate 9.2 files, without disabling segmentation', async () => {
    const app=buildApp({profileDir:'/missing-gate9-3-profile-directory'});
    const dash=await app.inject({method:'GET',url:'/api/dashboard'});
    expect(dash.statusCode).toBe(503);
    expect(dash.json()).toMatchObject({status:'not_ready'});
    const health=await app.inject({method:'GET',url:'/api/health'});
    expect(health.json().modelReady).toBe(true);
    const predicted=await app.inject({method:'POST',url:'/api/segment',payload:example});
    expect(predicted.statusCode).toBe(200);
    await app.close();
  });
});

describe('Gate 9.5: source-grounded model and data cards', () => {
  it('returns units, source, timing, frozen configuration and usage boundaries', async () => {
    const app = buildApp();
    const response = await app.inject({ method:'GET', url:'/api/model-info' });
    expect(response.statusCode).toBe(200);
    const info = response.json();
    expect(info).toMatchObject({
      status:'ready', selection_decision:'D011', k:2, training_count:352,
      data_card:{
        dataset:'Wholesale customers', uci_id:292, row_count:440,
        license:'CC BY 4.0', spending_period:'annual',
        spending_unit:'monetary units (m.u.)', currency_known:false,
        profiling_only_columns:['Channel','Region'],
      },
      model_card:{
        decision:'D011', algorithm:'KMeans (lloyd)', random_state:42,
        n_init:10, max_iter:300, k:2, fit_rows:352,
        held_out_test_rows:88, held_out_test_evaluated_once:true,
      },
    });
    expect(info.data_card.feature_columns).toEqual([
      'Fresh','Milk','Grocery','Frozen','Detergents_Paper','Delicassen'
    ]);
    expect(info.data_card.doi).toBe('https://doi.org/10.24432/C5030X');
    expect(info.data_card.data_available_when).toContain('đầy đủ chi tiêu hằng năm');
    expect(info.model_card.metric_cautions).toContain('Inertia raw và scaled');
    expect(info.model_card.distance_cautions).toContain('264 mẫu EDA');
    expect(info.model_card.prohibited_inferences).toContain('Không dùng cụm');
    expect(info.model_card.selection_rationale).toContain('K=2');
    const segment = await app.inject({
      method:'POST', url:'/api/segment', payload:example,
    });
    expect(segment.statusCode).toBe(200);
    expect([0,1]).toContain(segment.json().cluster_id);
    await app.close();
  });

  it('does not claim a specific currency or probabilistic confidence', async () => {
    const app = buildApp();
    const info = (await app.inject({ method:'GET', url:'/api/model-info' })).json();
    expect(info.data_card.currency_known).toBe(false);
    expect(info.data_card.spending_unit).not.toMatch(/VND|USD|EUR/i);
    expect(info.model_card.distance_cautions.toLowerCase()).toContain('không phải xác suất');
    expect(info.model_card.cluster_labels).toContain('không có thứ bậc');
    await app.close();
  });
});
