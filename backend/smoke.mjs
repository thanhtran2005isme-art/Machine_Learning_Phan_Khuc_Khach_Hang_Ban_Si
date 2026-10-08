import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { strict as assert } from 'node:assert';

const root = fileURLToPath(new URL('../', import.meta.url));
const port = 31947;
const base = 'http://127.0.0.1:' + port;
const child = spawn(process.execPath, ['backend/dist/server.js'], {
  cwd: root, env: { ...process.env, PORT: String(port), HOST: '127.0.0.1' },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let errorOutput = '';
child.stderr.on('data', buf => { errorOutput += String(buf).slice(-1000); });
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function request(route, options) {
  const res = await fetch(base + route, options);
  const body = await res.json();
  return { code: res.status, body };
}
try {
  let healthy = false;
  for (let i = 0; i < 40; i++) {
    if (child.exitCode !== null) throw new Error('Backend exited prematurely: ' + errorOutput);
    try {
      const health = await request('/api/health');
      if (health.code === 200 && health.body.modelReady) { healthy = true; break; }
    } catch { /* process not listening yet */ }
    await sleep(125);
  }
  assert.equal(healthy, true, 'Production backend modelReady must be true: ' + errorOutput);
  const info = await request('/api/model-info');
  assert.equal(info.code, 200);
  assert.equal(info.body.k, 2);
  const dashboard = await request('/api/dashboard');
  assert.equal(dashboard.code, 200);
  assert.equal(dashboard.body.experiments.length, 14);
  assert.equal(dashboard.body.final_profile.development_count, 352);
  assert.deepEqual(dashboard.body.final_profile.cluster_sizes.map(r => r.count), [162, 190]);
  assert.equal(dashboard.body.final_profile.channel_profile.reduce((n,r) => n + r.count,0),352);
  assert.equal(dashboard.body.final_profile.region_profile.reduce((n,r) => n + r.count,0),352);
  const example = { Fresh: 6410.5, Milk: 7226, Grocery: 10842.5, Frozen: 1153, Detergents_Paper: 4084.5, Delicassen: 1508.5 };
  const predicted = await request('/api/segment', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(example) });
  assert.equal(predicted.code, 200);
  assert.ok(predicted.body.cluster_id === 0 || predicted.body.cluster_id === 1);
  assert.ok(Number.isFinite(predicted.body.distance_to_centroid));
  const rejected = await request('/api/segment', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ Fresh: -1 }) });
  assert.equal(rejected.code, 400);
  console.log('PASS production HTTP smoke: health, model-info, dashboard, segment, invalid input');
} finally {
  child.kill('SIGTERM');
}
