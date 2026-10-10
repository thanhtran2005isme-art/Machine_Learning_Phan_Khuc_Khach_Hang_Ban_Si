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


test('Gate 9.4 chart values are grounded in the verified final API profile', async ({ page, request }) => {
  const api = await request.get('/api/dashboard');
  expect(api.status()).toBe(200);
  const { final_profile: profile } = await api.json();
  await page.goto('/');
  await page.getByRole('button', { name: 'Dashboard', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'So sánh median chi tiêu' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Quy mô hai cụm' })).toBeVisible();
  const size = page.getByRole('img', { name: /^Quy mô cụm:/ });
  const label = await size.getAttribute('aria-label');
  expect(label).toContain('cụm 0 ' + profile.cluster_sizes[0].count + ' khách');
  expect(label).toContain('cụm 1 ' + profile.cluster_sizes[1].count + ' khách');
  const medians = await page.getByRole('img', { name: /^Tỷ lệ median theo cụm/ }).getAttribute('aria-label');
  expect(medians).toContain('Fresh cụm 0 ' + profile.median_ratio[0].values.Fresh.toFixed(3));
  expect(medians).toContain('Detergents_Paper cụm 0 ' + profile.median_ratio[0].values.Detergents_Paper.toFixed(3) + ', cụm 1 ' + profile.median_ratio[1].values.Detergents_Paper.toFixed(3));
  await expect(page.getByRole('heading', { name: 'Median chi tiêu gốc theo cụm' })).toBeVisible();
  await expect(page.getByRole('heading', { name: profile.cluster_summary[0].name })).toBeVisible();
  await expect(page.getByRole('heading', { name: profile.cluster_summary[1].name })).toBeVisible();
});

test('Gate 9.4 Channel and Region charts show the original category counts and percentages', async ({ page, request }) => {
  const { final_profile: profile } = await (await request.get('/api/dashboard')).json();
  await page.goto('/');
  await page.getByRole('button', { name: 'Dashboard', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Phân bố Channel' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Phân bố Region' })).toBeVisible();
  const channel = await page.getByRole('img', { name: /^Phân bố Channel, cụm 0/ }).getAttribute('aria-label');
  expect(channel).toContain(profile.channel_profile.find((x: { cluster_id: number; channel: number }) =>
    x.cluster_id === 0 && x.channel === 1).count + ' khách');
  const region = await page.getByRole('img', { name: /^Phân bố Region, cụm 1/ }).getAttribute('aria-label');
  expect(region).toContain(profile.region_profile.find((x: { cluster_id: number; region: number }) =>
    x.cluster_id === 1 && x.region === 3).count + ' khách');
  await expect(page.getByRole('table', { name: 'Phân bố Channel theo số lượng và tỷ trọng từng cụm' })).toBeVisible();
  await expect(page.getByRole('table', { name: 'Phân bố Region theo số lượng và tỷ trọng từng cụm' })).toBeVisible();
});

test('Gate 9.4 distance plot and outlier breakdown match API without treating distances as confidence', async ({ page, request }) => {
  const { final_profile: profile } = await (await request.get('/api/dashboard')).json();
  await page.goto('/');
  await page.getByRole('button', { name: 'Dashboard', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Khoảng cách tới tâm cụm' })).toBeVisible();
  const labels = await page.getByRole('img', { name: /^Khoảng cách tới tâm cụm:/ }).getAttribute('aria-label');
  expect(labels).toContain('cụm 0 trung vị ' + profile.distance_summary[0].median.toFixed(3));
  expect(labels).toContain('cụm 1 trung vị ' + profile.distance_summary[1].median.toFixed(3));
  expect(labels).toContain('ngoại lệ IQR ' + profile.distance_summary[1].iqr_distance_outlier_count);
  await expect(page.getByRole('table', { name: 'Thống kê khoảng cách của mô hình cuối' })).toBeVisible();
  await expect(page.getByText('Tổng ' + profile.outliers.count + ' mẫu ngoài ngưỡng')).toBeVisible();
});

test('Gate 9.4 K explorer browses all candidates without changing K=2 serving', async ({ page, request }) => {
  const api = await request.get('/api/dashboard');
  const evidence = await api.json();
  const explorer = (await page.goto('/'), await page.getByRole('button', { name: 'Dashboard', exact: true }).click(),
    page.getByRole('region', { name: 'Khám phá cấu hình K' }));
  await expect(explorer).toBeVisible();
  const controls = page.getByRole('group', { name: 'Chọn K để xem thí nghiệm' });
  const serving = page.getByText('D011 · Mô hình được chọn');
  await expect(serving).toBeVisible();
  for (const k of [3, 5, 8]) {
    await controls.getByRole('button', { name: 'K=' + k, exact: true }).click();
    await expect(controls.getByRole('button', { name: 'K=' + k })).toHaveAttribute('aria-pressed', 'true');
    const entry = evidence.experiments.find((e: { k: number; preprocessing: string }) =>
      e.k === k && e.preprocessing === 'log1p_standardscaler');
    await expect(page.getByTestId('candidate-inertia')).toHaveText(
      entry.train_inertia.toLocaleString('vi-VN', { maximumFractionDigits: 2 }));
    await expect(serving).toHaveCount(0);
  }
  await page.getByRole('button', { name: 'Raw', exact: true }).click();
  const raw = evidence.experiments.find((e: { k: number; preprocessing: string }) =>
    e.k === 8 && e.preprocessing === 'raw');
  await expect(page.getByTestId('candidate-silhouette')).toHaveText(
    raw.validation_silhouette.toLocaleString('vi-VN', { maximumFractionDigits: 4 }));
  await controls.getByRole('button', { name: 'K=2', exact: true }).click();
  await expect(serving).toHaveCount(0);
  await page.getByRole('button', { name: 'Log1p + StandardScaler', exact: true }).click();
  await expect(serving).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Hồ sơ 2 phân khúc cuối' })).toBeVisible();
  await expect(page.getByText('K phục vụ luôn cố định: 2.')).toBeVisible();
  const prediction = await request.post('/api/segment', { data: sample });
  expect(prediction.ok()).toBeTruthy();
  expect([0,1]).toContain((await prediction.json()).cluster_id);
});

test('Gate 9.4 denies misleading visuals if final profile is missing from API 200', async ({ page }) => {
  await page.route('**/api/dashboard', async route => {
    const response = await route.fetch();
    const original = await response.json();
    delete original.final_profile;
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(original) });
  });
  await page.goto('/');
  await page.getByRole('button', { name: 'Dashboard', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('Hồ sơ phân khúc cuối thiếu hoặc không hợp lệ');
  await expect(page.getByRole('heading', { name: 'Quy mô hai cụm' })).toHaveCount(0);
  await expect(page.getByRole('heading', { name: 'So sánh median chi tiêu' })).toHaveCount(0);
});

test('Gate 9.4 has no document overflow at narrow 320px while tables scroll internally', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 720 });
  await page.goto('/');
  await page.getByRole('button', { name: 'Dashboard', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'So sánh median chi tiêu' })).toBeVisible();
  const widths = await page.evaluate(() => ({
    doc: document.documentElement.scrollWidth, viewport: window.innerWidth,
    tables: [...document.querySelectorAll<HTMLElement>('.table-scroll')].map(x => x.scrollWidth >= x.clientWidth),
  }));
  expect(widths.doc).toBeLessThanOrEqual(widths.viewport + 1);
  expect(widths.tables.length).toBeGreaterThanOrEqual(4); // Multiple verified development tables added in Gate10.2.
  expect(widths.tables.every(Boolean)).toBeTruthy();
});

test('Gate 9.5 data card identifies UCI monetary units, source and annual-record requirement', async ({ page, request }) => {
  const response = await request.get('/api/model-info');
  expect(response.ok()).toBeTruthy();
  const {data_card} = await response.json();
  await page.goto('/');
  await expect(page.getByRole('heading', { name:'Data card' })).toBeVisible();
  await expect(page.getByText(data_card.spending_unit, { exact:false }).first()).toBeVisible();
  const link = page.getByRole('link', { name:'Nguồn dữ liệu UCI' });
  await expect(link).toHaveAttribute('href', data_card.source_url);
  await expect(page.getByText(data_card.data_available_when)).toBeVisible();
  await page.getByRole('button', { name:'Phân khúc', exact:true }).click();
  await expect(page.getByText(/monetary units.*không mặc định VND/)).toBeVisible();
});

test('Gate 9.5 final model card uses configuration from API and explains selection/limitations', async ({ page, request }) => {
  const info = await (await request.get('/api/model-info')).json();
  await page.goto('/');
  await page.getByRole('button', { name:'Dashboard', exact:true }).click();
  await expect(page.getByRole('heading', { name:'Model card' })).toBeVisible();
  await expect(page.getByText('KMeans (lloyd)')).toBeVisible();
  const facts = page.locator('.model-facts');
  await expect(facts).toContainText(String(info.model_card.random_state));
  await expect(facts).toContainText(String(info.model_card.n_init));
  await expect(facts).toContainText(String(info.model_card.max_iter));
  await expect(page.getByRole('heading', { name:'Vì sao chọn K=2?' })).toBeVisible();
  await expect(page.getByText(info.model_card.selection_rationale)).toBeVisible();
  await expect(page.getByText(info.model_card.metric_cautions)).toBeVisible();
  await expect(page.getByText(info.model_card.distance_cautions)).toBeVisible();
});

test('Gate 9.5 result states neutral group meaning without replacing centroid distance', async ({ page }) => {
  await openSegment(page);
  await exampleInput(page);
  await page.getByRole('button', { name:'Phân khúc khách hàng', exact:true }).click();
  const result = page.locator('.result-card');
  await expect(result).toBeVisible();
  await expect(result).toContainText('Tên cụm mô tả xu hướng chi tiêu');
  await expect(result).toContainText('Khoảng cách không phải xác suất hoặc độ tin cậy');
});


test('Gate 10.1 guided Lloyd example is not the serving model', async ({page})=>{
  await page.goto('/');
  const toy=page.getByRole('region',{name:'Minh họa Lloyd với điểm mô phỏng'});
  await expect(toy.getByRole('heading',{name:'K-Means hoạt động như thế nào?'})).toBeVisible();
  await toy.getByRole('button',{name:'Bước tiếp'}).click();
  await expect(toy.getByRole('heading',{name:/Cập nhật tâm/})).toBeVisible();
  await toy.getByRole('button',{name:'Bước tiếp'}).click();
  await expect(toy.getByText(/Chi chuyển sang cụm 0/)).toBeVisible();
});
test('Gate 10.1 extended experiments use 14 verified rows and export CSV',async ({page,request})=>{
  const response=await request.get('/api/dashboard');
  expect(response.ok()).toBeTruthy();
  const evidence=await response.json();
  expect(evidence.experiments.every((x:{pair_count:number})=>x.pair_count===45)).toBe(true);
  await page.goto('/');
  await page.getByRole('button',{name:'Dashboard',exact:true}).click();
  const report=page.getByRole('region',{name:'Bảng bằng chứng thí nghiệm chuyên sâu'});
  await expect(report.getByRole('heading',{name:'Bảng thí nghiệm chuyên sâu'})).toBeVisible();
  await expect(report.locator('tbody tr')).toHaveCount(14);
  const file=page.waitForEvent('download');
  await report.getByRole('button',{name:'Tải CSV thí nghiệm'}).click();
  expect((await file).suggestedFilename()).toBe('kaitokidshop-thi-nghiem.csv');
});
test('Gate 10.1 segment explains six spending values and exports CSV',async ({page})=>{
  await openSegment(page);await exampleInput(page);
  await page.getByRole('button',{name:'Phân khúc khách hàng',exact:true}).click();
  const card=page.locator('.result-card');
  await expect(card.getByRole('heading',{name:'Giải thích kết quả từng khách'})).toBeVisible();
  await expect(card.locator('.analysis-extra tbody tr')).toHaveCount(6);
  const file=page.waitForEvent('download');
  await card.getByRole('button',{name:'Tải CSV kết quả'}).click();
  expect((await file).suggestedFilename()).toBe('kaitokidshop-ket-qua-phan-khuc.csv');
});


test('Gate 10.2 PCA plots 352 real development points and filters by split',async({page,request})=>{
  const reply=await request.get('/api/development-extension');
  expect(reply.status()).toBe(200);
  const data=await reply.json();
  expect(data.points).toHaveLength(352);
  expect(data.comparison.frozen_counts).toEqual([162,190]);
  await page.goto('/');
  await page.getByRole('button',{name:'Dashboard',exact:true}).click();
  const panel=page.getByRole('region',{name:'PCA 2D và so sánh Hierarchical'});
  await expect(panel.getByRole('heading',{name:/PCA 2D · So sánh/})).toBeVisible();
  await expect(panel.locator('svg circle.pca-dot')).toHaveCount(352);
  await expect(panel.getByTestId('pca-visible-count')).toHaveText('352');
  await panel.getByRole('group',{name:'Lọc dữ liệu development'}).getByRole('button',{name:'Validation'}).click();
  await expect(panel.locator('svg circle.pca-dot')).toHaveCount(88);
  await panel.getByRole('group',{name:'Lọc dữ liệu development'}).getByRole('button',{name:'Train'}).click();
  await expect(panel.locator('svg circle.pca-dot')).toHaveCount(264);
  await panel.getByRole('group',{name:'Phương pháp tô màu'}).getByRole('button',{name:'Hierarchical Ward'}).click();
  expect(await panel.locator('svg circle[data-label="0"]').count()).toBeGreaterThan(0);
  await expect(panel.getByText(/Adjusted Rand Index/)).toBeVisible();
});


test('Gate 10.3 professional workspace navigates all three screens and shows verified sidebar state', async ({page}) => {
  await page.goto('/');
  await expect(page.locator('.site-header .brand')).toContainText('KaitoKidShop');
  await expect(page.getByText('Model D011 · Chỉ đọc')).toBeVisible();
  await page.getByRole('button',{name:'Phân khúc',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Phân khúc khách hàng mới'})).toBeVisible();
  await expect(page.getByText('0/6 trường')).toBeVisible();
  await page.getByRole('button',{name:'Điền ví dụ cụm 0'}).click();
  await expect(page.getByText('6/6 trường')).toBeVisible();
  await expect(page.locator('.input-grid .field-input')).toHaveCount(6);
  await page.getByRole('button',{name:'Dashboard',exact:true}).click();
  const shortcuts=page.getByRole('navigation',{name:'Truy cập nhanh các phân tích'});
  await expect(shortcuts.getByRole('link',{name:'PCA & Ward'})).toHaveAttribute('href','#pca-analysis');
  await expect(page.locator('#cluster-profiles')).toBeVisible();
  await page.getByRole('button',{name:'Giới thiệu',exact:true}).click();
  await expect(page.locator('.hero-preview')).toContainText('352 khách');
});

test('Gate 10.3 PCA allows selecting a real anonymous point by index',async({page})=>{
  await page.goto('/');
  await page.getByRole('button',{name:'Dashboard',exact:true}).click();
  const panel=page.getByRole('region',{name:'PCA 2D và so sánh Hierarchical'});
  await panel.getByLabel('Mã mẫu (1–352)').fill('352');
  await expect(panel.locator('.pca-point-detail')).toContainText('352');
  await expect(panel.locator('.pca-point-detail')).toContainText('Validation');
  await panel.getByLabel('Mã mẫu (1–352)').fill('0');
  await expect(panel.locator('.pca-point-detail')).toHaveCount(0);
});

test('Gate 10.3 responsive workspace has no horizontal overflow at 320px and 768px',async({page})=>{
  for (const width of [320,768]){
    await page.setViewportSize({width,height:780});
    await page.goto('/');
    for(const screen of ['Giới thiệu','Phân khúc','Dashboard']){
      await page.getByRole('button',{name:screen,exact:true}).click();
      if(screen==='Dashboard') await expect(page.locator('#cluster-profiles')).toBeVisible();
      const dimension=await page.evaluate(()=>({doc:document.documentElement.scrollWidth,viewport:innerWidth}));
      expect(dimension.doc).toBeLessThanOrEqual(dimension.viewport+1);
    }
  }
});
