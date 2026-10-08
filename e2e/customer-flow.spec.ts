import { test, expect } from '@playwright/test';

const sample = {
  Fresh: 6410.5,
  Milk: 7226,
  Grocery: 10842.5,
  Frozen: 1153,
  Detergents_Paper: 4084.5,
  Delicassen: 1508.5,
};

async function openSegment(page: import('@playwright/test').Page) {
  await page.goto('/');
  await page.getByRole('button', { name: 'Phân khúc', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Phân khúc khách hàng mới' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Điền ví dụ cụm 0' })).toBeVisible();
}
async function exampleInput(page: import('@playwright/test').Page) {
  await page.getByRole('button', { name: 'Điền ví dụ cụm 0' }).click();
}

test('landing screen explains frozen model and offers navigation', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /Hiểu cơ cấu chi tiêu/ })).toBeVisible();
  await expect(page.getByText('440', { exact: true })).toBeVisible();
  await expect(page.getByText('352', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Thử phân khúc khách hàng' }).click();
  await expect(page.getByRole('heading', { name: 'Phân khúc khách hàng mới' })).toBeVisible();
});

test('real end-to-end form predicts same cluster and profile as API', async ({ page, request }) => {
  await openSegment(page);
  await exampleInput(page);
  const api = await request.post('/api/segment', { data: sample });
  expect(api.ok()).toBeTruthy();
  const expected = await api.json();
  const fromUI = page.waitForResponse(r => r.url().endsWith('/api/segment') && r.request().method() === 'POST');
  await page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true }).click();
  const res = await fromUI;
  expect(res.ok()).toBeTruthy();
  const submitted = await res.json();
  expect(submitted.cluster_id).toBe(expected.cluster_id);
  expect(submitted.profile.name).toBe(expected.profile.name);
  expect(Math.abs(submitted.distance_to_centroid - expected.distance_to_centroid)).toBeLessThan(1e-10);
  const result = page.locator('.result-card');
  await expect(result.getByText('Cụm ' + expected.cluster_id, { exact: true })).toBeVisible();
  await expect(result.getByRole('heading', { name: expected.profile.name })).toBeVisible();
  await expect(result.getByText(/Khoảng cách tới tâm cụm/)).toBeVisible();
});

test('missing and negative values are rejected without sending a request', async ({ page }) => {
  await openSegment(page);
  await exampleInput(page);
  await page.locator('input').first().fill('');
  await page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('Vui lòng nhập đủ 6');
  await expect(page.locator('.result-card')).toHaveCount(0);
  await page.locator('input').first().fill('-1');
  await page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('không âm');
  await expect(page.locator('.result-card')).toHaveCount(0);
});

test('out-of-train range predicts but warns rather than clipping', async ({ page }) => {
  await openSegment(page);
  await exampleInput(page);
  await page.locator('input').first().fill('100000000');
  await page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true }).click();
  await expect(page.locator('.result-card')).toBeVisible();
  await expect(page.getByRole('status')).toContainText('Fresh: ngoài khoảng quan sát');
});

test('reset clears all inputs and removes previous result', async ({ page }) => {
  await openSegment(page);
  await exampleInput(page);
  await page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true }).click();
  await expect(page.locator('.result-card')).toBeVisible();
  await page.getByRole('button', { name: 'Xóa dữ liệu' }).click();
  await expect(page.locator('.result-card')).toHaveCount(0);
  for (const input of await page.locator('.input-grid input').all()) await expect(input).toHaveValue('');
});

test('dashboard renders real experiment rows and changes curves per preprocessing', async ({ page, request }) => {
  const api = await request.get('/api/dashboard');
  expect(api.ok()).toBeTruthy();
  const evidence = await api.json();
  expect(evidence.experiments).toHaveLength(14);
  await page.goto('/');
  await page.getByRole('button', { name: 'Dashboard', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Dashboard đánh giá K-Means' })).toBeVisible();
  const elbow = page.getByRole('img', { name: /^Elbow/ });
  await expect(elbow).toBeVisible();
  await expect(page.getByRole('img', { name: /^Validation silhouette/ })).toBeVisible();
  await expect(page.getByRole('img', { name: /^ARI stability/ })).toBeVisible();
  const logCurve = await elbow.getAttribute('aria-label');
  expect(logCurve).toContain('K 2 = ');
  expect(logCurve).toContain(evidence.experiments.find((x: { preprocessing: string; k: number }) =>
    x.preprocessing === 'log1p_standardscaler' && x.k === 2).train_inertia.toFixed(4));
  await page.getByRole('button', { name: 'Raw', exact: true }).click();
  const rawCurve = await elbow.getAttribute('aria-label');
  expect(rawCurve).not.toBe(logCurve);
  expect(rawCurve).toContain(evidence.experiments.find((x: { preprocessing: string; k: number }) =>
    x.preprocessing === 'raw' && x.k === 2).train_inertia.toFixed(4));
  await expect(page.getByRole('heading', { name: 'Hồ sơ 2 phân khúc cuối' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Model card' })).toBeVisible();
});

test('API missing fails visibly instead of presenting a fictitious model', async ({ page }) => {
  await page.route('**/api/model-info', route => route.fulfill({
    status: 503, contentType: 'application/json',
    body: JSON.stringify({ status: 'not_ready', message: 'Model unavailable' }),
  }));
  await page.goto('/');
  await expect(page.getByRole('alert')).toContainText('Không tải được mô hình');
  await page.getByRole('button', { name: 'Phân khúc', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true })).toBeDisabled();
});

test('dashboard API outage is explicitly reported', async ({ page }) => {
  await page.route('**/api/dashboard', route => route.fulfill({
    status: 503, contentType: 'application/json',
    body: JSON.stringify({ status: 'not_ready', message: 'Experiment evidence unavailable' }),
  }));
  await page.goto('/');
  await page.getByRole('button', { name: 'Dashboard', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('Experiment evidence unavailable');
});

test('no horizontal overflow at viewport size', async ({ page }) => {
  await page.goto('/');
  for (const label of ['Giới thiệu', 'Phân khúc', 'Dashboard']) {
    await page.getByRole('button', { name: label, exact: true }).click();
    if (label === 'Dashboard') await expect(page.getByRole('heading', { name: 'Model card' })).toBeVisible();
    const sizes = await page.evaluate(() => ({ doc: document.documentElement.scrollWidth, inner: window.innerWidth }));
    expect(sizes.doc).toBeLessThanOrEqual(sizes.inner + 1);
  }
});

test('old API response cannot restore a cleared or edited prediction', async ({ page }) => {
  await openSegment(page);
  await exampleInput(page);
  let release!: () => void;
  let intercepted!: () => void;
  const held = new Promise<void>(resolve => { release = resolve; });
  const interceptedRequest = new Promise<void>(resolve => { intercepted = resolve; });
  await page.route('**/api/segment', async route => {
    intercepted();
    await held;
    await route.continue();
  });
  const response = page.waitForResponse(r => r.url().endsWith('/api/segment') && r.request().method() === 'POST');
  await page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true }).click();
  await interceptedRequest;
  await page.getByRole('button', { name: 'Xóa dữ liệu' }).click();
  await expect(page.locator('.result-card')).toHaveCount(0);
  release();
  await response;
  await page.waitForTimeout(100);
  await expect(page.locator('.result-card')).toHaveCount(0);
  await expect(page.locator('.empty-result')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Phân khúc khách hàng', exact: true })).toBeEnabled();
});

test('Gate 9.3 dashboard API provides checksum-verified final 352-development data without changing selected K', async ({ request }) => {
  const response = await request.get('/api/dashboard');
  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body.k).toBe(2);
  expect(body.preprocessing).toBe('log1p_standardscaler');
  expect(body.experiments).toHaveLength(14);
  expect(body.final_profile).toMatchObject({
    development_count: 352,
    source_scope: 'train_plus_validation',
    profiling_only_columns: ['Channel', 'Region'],
    test_used: false,
    read_only: true,
  });
  expect(body.final_profile.cluster_sizes.map((r: {count: number}) => r.count)).toEqual([162, 190]);
  expect(body.final_profile.cluster_summary).toHaveLength(2);
  expect(body.final_profile.median_ratio).toHaveLength(2);
  expect(body.final_profile.distance_summary).toHaveLength(2);
  expect(body.final_profile.outliers.count).toBe(16);
  expect(body.final_profile.channel_profile.reduce((n: number, r: {count: number}) => n + r.count, 0)).toBe(352);
  expect(body.final_profile.region_profile.reduce((n: number, r: {count: number}) => n + r.count, 0)).toBe(352);
  expect(Object.keys(body.final_profile.evidence_sha256)).toHaveLength(6);
});
