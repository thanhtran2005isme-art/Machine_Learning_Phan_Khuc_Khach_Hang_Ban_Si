import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { loadModel, segment, dashboard } from './model.mjs';
const loaded = loadModel();
const spend = Object.fromEntries(loaded.model.feature_columns.map((f, i) => [f, [6410.5,7226,10842.5,1153,4084.5,1508.5][i]]));
const developmentExample = Object.fromEntries(loaded.model.feature_columns.map((feature, i) => {
  const midpoint = (loaded.model.cluster_centers[0][i] + loaded.model.cluster_centers[1][i]) / 2;
  return [feature, Math.max(0, Math.expm1(midpoint * loaded.model.scaler_scale[i] + loaded.model.scaler_mean[i]))];
}));
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
  assert.equal(result.decision_support.status, 'descriptive');
  assert.equal(result.decision_support.priority, 'low');
  assert.deepEqual(result.out_of_train_range_features, []);
  assert.equal(result.alternative_profile.name, loaded.model.cluster_profiles[1 - result.cluster_id].profile_name);
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
test('business diagnostics separate boundary review from out-of-domain review', () => {
  const boundary = segment(loaded, developmentExample);
  assert.equal(boundary.cluster_id, 0, 'sklearn tie rule keeps the first centroid');
  assert.ok(boundary.relative_margin < 1e-12);
  assert.ok(boundary.decision_support.reason_codes.includes('near_boundary'));
  assert.equal(boundary.decision_support.priority, 'medium');
  assert.equal(boundary.alternative_profile.name, loaded.model.cluster_profiles[1].profile_name);

  const outOfDomain = segment(loaded, { ...spend, Fresh: 1e8 });
  assert.ok(outOfDomain.decision_support.reason_codes.includes('out_of_train_range'));
  assert.ok(outOfDomain.decision_support.reason_codes.includes('high_distance'));
  assert.equal(outOfDomain.decision_support.priority, 'high');
  assert.equal(outOfDomain.out_of_train_range_features[0], 'Fresh');
  assert.ok(outOfDomain.distance_ratio_to_development_rms > 1.5);
});
test('dashboard contains real fourteen experiment rows', () => {
  assert.equal(dashboard(loaded).experiments.length, 14);
});

test('rejects tampering of the frozen model despite valid JSON', async () => {
  const { mkdtempSync, writeFileSync, rmSync, readFileSync } = await import('node:fs');
  const { tmpdir } = await import('node:os');
  const { join } = await import('node:path');
  const directory = mkdtempSync(join(tmpdir(), 'gate6-integrity-'));
  try {
    const path = join(directory, 'tampered.json');
    const original = readFileSync(new URL('../models/model.json', import.meta.url), 'utf8');
    const modified = JSON.parse(original);
    modified.cluster_centers[0][0] += 0.000001;
    writeFileSync(path, JSON.stringify(modified), 'utf8');
    assert.throws(() => loadModel({ modelPath: path }), /checksum mismatch/);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});
