import { test } from 'node:test';
import { strict as assert } from 'node:assert';
import { spawnSync } from 'node:child_process';
import { loadModel, segment } from './model.mjs';

test('Gate 7: frozen sklearn joblib predictions and centroid distances match Node JSON serving', () => {
  const python = process.env.PYTHON || (process.platform === 'win32' ? 'py' : 'python');
  const commandArgs = [...(python === 'py' ? ['-3'] : []), 'ml/tests/gate7_parity_reference.py'];
  const result = spawnSync(python, commandArgs, { encoding: 'utf8', timeout: 30_000 });
  assert.equal(result.status, 0, 'Python reference failed: ' + (result.stderr || result.error?.message || 'unknown'));
  const data = JSON.parse(result.stdout);
  const loaded = loadModel();
  assert.deepEqual(data.features, loaded.model.feature_columns);
  assert.equal(data.inputs.length, 6);
  for (let j = 0; j < data.inputs.length; j++) {
    const spending = Object.fromEntries(data.features.map((f, i) => [f, data.inputs[j][i]]));
    const actual = segment(loaded, spending);
    assert.equal(actual.cluster_id, data.labels[j], 'cluster mismatch case ' + j);
    for (let k = 0; k < 2; k++) {
      assert.ok(Math.abs(actual.distances_to_centroids[k] - data.distances[j][k]) < 1e-8,
        'distance mismatch case ' + j + ' cluster ' + k);
    }
  }
});
