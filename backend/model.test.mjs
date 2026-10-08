import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { loadModel, segment, dashboard } from './model.mjs';
const loaded = loadModel();
const spend = Object.fromEntries(loaded.model.feature_columns.map((f, i) => [f, [6410.5,7226,10842.5,1153,4084.5,1508.5][i]]));
test('frozen JSON integrity and selection', () => {
  assert.equal(loaded.model.k, 2);
  assert.equal(loaded.evaluation.status, 'COMPLETE');
  assert.equal(loaded.model.training_count, 352);
});
test('predictions match an independent direct centroid calculation', () => {
  const z = loaded.model.feature_columns.map((f, i) => (Math.log1p(spend[f]) - loaded.model.scaler_mean[i]) / loaded.model.scaler_scale[i]);
  const expected = loaded.model.cluster_centers.map(c => Math.hypot(...z.map((x, i) => x - c[i])));
  const result = segment(loaded, spend);
  expected.forEach((x, i) => assert.ok(Math.abs(x - result.distances_to_centroids[i]) < 1e-10));
  assert.equal(result.cluster_id, expected[1] < expected[0] ? 1 : 0);
});
test('no input mutation, no coercion, warning not clipping', () => {
  const before = JSON.stringify(spend);
  segment(loaded, spend);
  assert.equal(JSON.stringify(spend), before);
  assert.throws(() => segment(loaded, { ...spend, Fresh: -2 }), TypeError);
  assert.throws(() => segment(loaded, { ...spend, Fresh: '50' }), TypeError);
  const outside = segment(loaded, { ...spend, Fresh: 1e8 });
  assert.ok(outside.warnings.some(w => w.startsWith('Fresh:')));
});
test('dashboard contains real fourteen experiment rows', () => {
  assert.equal(dashboard(loaded).experiments.length, 14);
});
