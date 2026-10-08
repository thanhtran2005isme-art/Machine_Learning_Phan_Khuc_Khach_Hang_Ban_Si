import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';

type Feature = 'Fresh' | 'Milk' | 'Grocery' | 'Frozen' | 'Detergents_Paper' | 'Delicassen';
type Screen = 'intro' | 'segment' | 'dashboard';
type Profile = { cluster_id: number; name: string; count: number; share: number; median_spending: Record<Feature, number> };
type ModelInfo = {
  status: string; k: number; preprocessing: string; training_count: number; artifact_sha256: string;
  profiles: Profile[]; reference_ranges: Record<Feature, { min: number; max: number }>;
  reference_note: string; limitations: string;
};
type SegmentResult = {
  status: string; cluster_id: number; distance_to_centroid: number; distances_to_centroids: number[];
  profile: { name: string; count: number; share: number; median_spending: Record<Feature, number> };
  warnings: string[]; distance_space: string;
};
type Experiment = {
  preprocessing: string; k: number; train_inertia: number;
  validation_silhouette: number; ari: number; min_cluster_share: number;
};
type Dashboard = {
  experiments: Experiment[]; training: { rows: number; silhouette: number; inertia_per_row: number };
  final_test: { rows: number; silhouette: number; inertia_per_row: number; cluster_counts: Record<string, number> };
  profiles: Profile[]; metric_note: string;
};
const FIELDS: { key: Feature; label: string; description: string }[] = [
  { key: 'Fresh', label: 'Hàng tươi', description: 'Fresh' },
  { key: 'Milk', label: 'Sữa', description: 'Milk' },
  { key: 'Grocery', label: 'Tạp hóa', description: 'Grocery' },
  { key: 'Frozen', label: 'Đông lạnh', description: 'Frozen' },
  { key: 'Detergents_Paper', label: 'Chất tẩy rửa & giấy', description: 'Detergents_Paper' },
  { key: 'Delicassen', label: 'Thực phẩm chế biến', description: 'Delicassen' },
];
const formatNumber = (value: number, digits = 0) =>
  new Intl.NumberFormat('vi-VN', { maximumFractionDigits: digits }).format(value);
const formatPercent = (value: number) => formatNumber(value * 100, 1) + '%';
async function getJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  const json: unknown = await response.json();
  if (!response.ok) {
    const error = json as { message?: string; detail?: string };
    throw new Error(error.message || error.detail || 'Yêu cầu thất bại (HTTP ' + response.status + ')');
  }
  return json as T;
}
function Chart({ title, description, rows, metric }: {
  title: string; description: string; rows: Experiment[]; metric: 'train_inertia' | 'validation_silhouette' | 'ari';
}) {
  const data = [...rows].sort((a,b) => a.k - b.k);
  if (data.length < 2) return <p className="muted">Không đủ dữ liệu biểu đồ.</p>;
  const nums = data.map(r => r[metric]);
  const lo = Math.min(...nums), hi = Math.max(...nums);
  const min = Math.max(0, lo - (hi - lo || hi * 0.1 || 1) * 0.2);
  const max = hi + (hi - lo || hi * 0.1 || 1) * 0.2;
  const y = (v: number) => 200 - ((v - min) / (max - min)) * 166;
  const x = (i: number) => 67 + i * (550 / (data.length - 1));
  const points = data.map((r,i) => x(i) + ',' + y(r[metric])).join(' ');
  return <section className="chart-card">
    <div className="section-heading"><h3>{title}</h3><p>{description}</p></div>
    <svg viewBox="0 0 680 245" role="img" aria-label={title + ': ' + data.map(r => 'K ' + r.k + ' = ' + r[metric].toFixed(4)).join(', ')}>
      {[0,1,2,3,4].map(step => <g key={step}>
        <line x1="65" x2="630" y1={34 + step * 41.5} y2={34 + step * 41.5} stroke="#e5e9f0" />
        <text x="56" y={39 + step * 41.5} textAnchor="end" fontSize="12" fill="#6b7280">{formatNumber(max - (max - min) * step / 4, metric === 'train_inertia' ? 0 : 3)}</text>
      </g>)}
      <polyline points={points} fill="none" stroke="#12735c" strokeWidth="3.2" strokeLinejoin="round" strokeLinecap="round" />
      {data.map((row,i) => <g key={row.k}>
        <circle cx={x(i)} cy={y(row[metric])} r="5" fill="#12735c" stroke="white" strokeWidth="2" />
        <text x={x(i)} y="224" textAnchor="middle" fontSize="13" fill="#4b5563">K={row.k}</text>
      </g>)}
    </svg>
  </section>;
}
function ProfileCard({ profile }: { profile: Profile }) {
  return <article className="profile-card">
    <div className="profile-header">
      <div><span className="eyebrow">Cụm {profile.cluster_id}</span><h3>{profile.name}</h3></div>
      <strong>{formatPercent(profile.share)}</strong>
    </div>
    <p className="muted">{formatNumber(profile.count)} khách trong tập huấn luyện cuối (352 khách)</p>
    <div className="profile-values">{FIELDS.map(f => <div key={f.key}>
      <span>{f.label}</span><strong>{formatNumber(profile.median_spending[f.key])}</strong>
    </div>)}</div>
  </article>;
}
export default function App() {
  const [screen, setScreen] = useState<Screen>('intro');
  const [info, setInfo] = useState<ModelInfo | null>(null);
  const [modelError, setModelError] = useState<string | null>(null);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [dashboardError, setDashboardError] = useState<string | null>(null);
  const [preprocessing, setPreprocessing] = useState('log1p_standardscaler');
  const [values, setValues] = useState<Record<Feature, string>>({
    Fresh: '', Milk: '', Grocery: '', Frozen: '', Detergents_Paper: '', Delicassen: '',
  });
  const [result, setResult] = useState<SegmentResult | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    getJson<ModelInfo>('/api/model-info').then(setInfo).catch(e => setModelError(String(e.message)));
  }, []);
  useEffect(() => {
    if (screen !== 'dashboard' || dashboard) return;
    getJson<Dashboard>('/api/dashboard').then(setDashboard).catch(e => setDashboardError(String(e.message)));
  }, [screen, dashboard]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitError(null); setResult(null);
    const spending: Partial<Record<Feature, number>> = {};
    for (const field of FIELDS) {
      const raw = values[field.key].trim();
      const parsed = Number(raw);
      if (!raw || !Number.isFinite(parsed) || parsed < 0) {
        setSubmitError('Vui lòng nhập đủ 6 giá trị số không âm, hữu hạn.');
        return;
      }
      spending[field.key] = parsed;
    }
    setSubmitting(true);
    try {
      const body = await getJson<SegmentResult>('/api/segment', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(spending),
      });
      setResult(body);
    } catch(e) {
      setSubmitError(e instanceof Error ? e.message : 'Không thể phân khúc');
    } finally { setSubmitting(false); }
  };

  const filledExample = (profile: Profile) => {
    setValues(Object.fromEntries(FIELDS.map(f => [f.key, String(profile.median_spending[f.key])])) as Record<Feature, string>);
    setResult(null); setSubmitError(null);
  };
  const allRows = dashboard?.experiments.filter(row => row.preprocessing === preprocessing) || [];

  return <div className="app-shell">
    <header className="site-header">
      <div className="container header-inner">
        <div className="brand"><span className="brand-mark">K</span><div><strong>KaitoKidShop</strong><small>Phân khúc khách hàng bán sỉ</small></div></div>
        <nav className="nav-tabs" aria-label="Điều hướng chính">
          {([{ id: 'intro', label: 'Giới thiệu' }, { id: 'segment', label: 'Phân khúc' }, { id: 'dashboard', label: 'Dashboard' }] as const).map(tab =>
            <button key={tab.id} className={screen === tab.id ? 'nav-active' : ''} onClick={() => setScreen(tab.id)} aria-current={screen === tab.id ? 'page' : undefined}>{tab.label}</button>)}
        </nav>
      </div>
    </header>
    <main className="container main-content">
      {modelError && <div className="notice notice-error" role="alert">Không tải được mô hình: {modelError}. Kiểm tra Backend và artifact Gate 5.</div>}
      {screen === 'intro' && <div className="intro">
        <section className="hero">
          <span className="eyebrow">PROJECT 22 · MACHINE LEARNING</span>
          <h1>Hiểu cơ cấu chi tiêu, nhận diện phân khúc khách hàng bán sỉ.</h1>
          <p>Dựa trên dữ liệu UCI Wholesale Customers, mô hình K-Means phân nhóm theo sáu loại chi tiêu hằng năm. Kết quả giúp khám phá đặc điểm nhóm, không đánh giá giá trị của một khách hàng.</p>
          <div className="hero-actions"><button className="btn-primary" onClick={() => setScreen('segment')}>Thử phân khúc khách hàng →</button><button className="btn-subtle" onClick={() => setScreen('dashboard')}>Xem kết quả thí nghiệm</button></div>
        </section>
        <div className="stat-grid">
          <article className="stat"><span>Khách hàng trong bộ dữ liệu</span><strong>440</strong><small>UCI Wholesale Customers</small></article>
          <article className="stat"><span>Biến chi tiêu sử dụng</span><strong>6</strong><small>Không dùng Channel/Region để fit</small></article>
          <article className="stat"><span>Số phân khúc cuối</span><strong>{info?.k ?? '—'}</strong><small>Quyết định D011, đã đóng băng</small></article>
          <article className="stat"><span>Mẫu huấn luyện cuối</span><strong>{info?.training_count ?? '—'}</strong><small>Train + validation</small></article>
        </div>
        <section className="content-card"><div className="section-heading"><h2>Phương pháp & giới hạn</h2><p>Mô hình sử dụng đúng artifact đã kiểm chứng, không huấn luyện lại theo mỗi yêu cầu.</p></div>
          <div className="three-columns">
            <div><h3>Tiền xử lý</h3><p>log1p → StandardScaler được fit trên tập development, áp dụng nhất quán cho khách mới.</p></div>
            <div><h3>Phân cụm</h3><p>K-Means K=2, trả mã cụm, khoảng cách Euclidean trong không gian chuẩn hóa và median chi tiêu.</p></div>
            <div><h3>Giới hạn</h3><p>{info?.limitations || 'K-Means mô tả nhóm, không phải dự đoán doanh thu hay đánh giá khách hàng.'}</p></div>
          </div>
        </section>
      </div>}
      {screen === 'segment' && <section>
        <div className="page-heading"><span className="eyebrow">01 / PHÂN KHÚC KHÁCH HÀNG</span><h1>Phân khúc khách hàng mới</h1><p>Nhập chi tiêu hằng năm của khách trong cùng đơn vị tiền tệ theo bộ dữ liệu UCI. Không quy đổi hoặc tự điền giá trị còn thiếu.</p></div>
        <div className="segment-grid">
          <form className="content-card" onSubmit={submit} noValidate>
            <div className="section-heading"><h2>Thông tin chi tiêu</h2><p>Sáu trường bắt buộc, mỗi giá trị là số không âm.</p></div>
            <div className="input-grid">{FIELDS.map(f => <label className="field" key={f.key}>
              <span>{f.label} <small>({f.description})</small></span>
              <input inputMode="decimal" type="number" min="0" step="any" required placeholder="Nhập số tiền" value={values[f.key]}
                onChange={event => { setValues(prev => ({ ...prev, [f.key]: event.target.value })); setResult(null); }} />
              <small>{info?.reference_ranges?.[f.key] ? 'Train quan sát: ' + formatNumber(info.reference_ranges[f.key].min) + ' – ' + formatNumber(info.reference_ranges[f.key].max) : 'Giá trị không âm'}</small>
            </label>)}</div>
            {submitError && <p className="notice notice-error" role="alert">{submitError}</p>}
            <div className="form-footer"><button className="btn-primary" type="submit" disabled={submitting || !info}>{submitting ? 'Đang xử lý…' : 'Phân khúc khách hàng'}</button><button className="btn-subtle" type="button" onClick={() => { setValues({ Fresh:'', Milk:'', Grocery:'', Frozen:'', Detergents_Paper:'', Delicassen:'' }); setResult(null); }}>Xóa dữ liệu</button></div>
            <p className="muted small-note">{info?.reference_note || 'Khoảng giá trị là thông tin tham khảo, không phải giới hạn đầu vào cứng.'}</p>
          </form>
          <div className="result-column">
            {result ? <article className="result-card" aria-live="polite">
              <span className="eyebrow">KẾT QUẢ MÔ HÌNH THỰC</span>
              <div className="result-id">Cụm {result.cluster_id}</div>
              <h2>{result.profile.name}</h2>
              <p>Khoảng cách tới tâm cụm: <strong>{formatNumber(result.distance_to_centroid, 4)}</strong></p>
              <p className="muted small-note">{result.distance_space}. Khoảng cách không phải xác suất hoặc độ tin cậy.</p>
              {result.warnings.length > 0 && <div className="notice notice-warn" role="status"><strong>Cảnh báo ngoài khoảng train:</strong>{result.warnings.map((w,i) => <p key={i}>{w}</p>)}</div>}
              <div className="divider-line" />
              <h3>Median chi tiêu của cụm</h3>
              <div className="profile-values">{FIELDS.map(f => <div key={f.key}><span>{f.label}</span><strong>{formatNumber(result.profile.median_spending[f.key])}</strong></div>)}</div>
            </article> : <div className="empty-result"><div className="empty-icon">◎</div><h2>Chưa có kết quả phân khúc</h2><p>Nhập 6 giá trị và nhấn “Phân khúc khách hàng”. Bạn cũng có thể dùng median thực từ mô hình làm dữ liệu ví dụ:</p><div className="example-actions">{info?.profiles.map(p => <button className="btn-subtle" key={p.cluster_id} onClick={() => filledExample(p)}>Điền ví dụ cụm {p.cluster_id}</button>)}</div></div>}
          </div>
        </div>
      </section>}
      {screen === 'dashboard' && <section>
        <div className="page-heading"><span className="eyebrow">02 / THÍ NGHIỆM & MÔ HÌNH</span><h1>Dashboard đánh giá K-Means</h1><p>Số liệu từ experiment artifacts và final evaluation đã đóng băng; không chạy lại mô hình hoặc final test.</p></div>
        {dashboardError && <div className="notice notice-error" role="alert">{dashboardError}</div>}
        {!dashboard && !dashboardError && <p className="muted">Đang tải dữ liệu thí nghiệm…</p>}
        {dashboard && <>
          <div className="stat-grid">
            <article className="stat"><span>K đã chọn</span><strong>2</strong><small>Log1p + StandardScaler</small></article>
            <article className="stat"><span>Silhouette development</span><strong>{formatNumber(dashboard.training.silhouette, 4)}</strong><small>{dashboard.training.rows} mẫu</small></article>
            <article className="stat"><span>Silhouette final test</span><strong>{formatNumber(dashboard.final_test.silhouette, 4)}</strong><small>Đã đánh giá một lần</small></article>
            <article className="stat"><span>Final test độc lập</span><strong>{dashboard.final_test.rows}</strong><small>Khách hàng, không tham gia fit</small></article>
          </div>
          <section className="content-card"><div className="section-heading"><h2>So sánh K=2..8</h2><p>Chọn một không gian để xem inertia; không so sánh trực tiếp trị số inertia giữa raw và scaled.</p></div>
            <div className="toggle-row"><button className={preprocessing === 'log1p_standardscaler' ? 'toggle-selected' : ''} onClick={() => setPreprocessing('log1p_standardscaler')}>Log1p + StandardScaler</button><button className={preprocessing === 'raw' ? 'toggle-selected' : ''} onClick={() => setPreprocessing('raw')}>Raw</button></div>
            <div className="charts"><Chart title="Elbow · Train inertia" description="Thấp hơn khi K tăng; dùng xem mức thay đổi trong cùng preprocessing." rows={allRows} metric="train_inertia" /><Chart title="Validation silhouette" description="Giá trị cao hơn biểu thị phân tách tốt hơn theo metric này." rows={allRows} metric="validation_silhouette" /><Chart title="ARI stability qua 10 seed" description="Độ nhất quán gán cụm giữa các lần khởi tạo." rows={allRows} metric="ari" /></div>
            <p className="muted small-note">{dashboard.metric_note}</p>
          </section>
          <section className="content-card"><div className="section-heading"><h2>Hồ sơ 2 phân khúc cuối</h2><p>Median chi tiêu theo đơn vị gốc, tính từ 352 khách train+validation.</p></div><div className="profile-grid">{dashboard.profiles.map(p => <ProfileCard key={p.cluster_id} profile={p} />)}</div></section>
          <section className="content-card"><div className="section-heading"><h2>Model card</h2><p>Trạng thái mô hình đã freeze trước final test.</p></div>
            <dl className="model-facts"><div><dt>Preprocessing</dt><dd>log1p + StandardScaler</dd></div><div><dt>Số cụm</dt><dd>2</dd></div><div><dt>Huấn luyện</dt><dd>352 khách (train + validation)</dd></div><div><dt>Final test</dt><dd>88 khách, silhouette {formatNumber(dashboard.final_test.silhouette, 6)}</dd></div><div><dt>Artifact SHA-256</dt><dd className="hash">{info?.artifact_sha256 || 'Đang tải…'}</dd></div></dl>
            <p className="muted small-note">{info?.limitations}</p>
          </section>
        </>}
      </section>}
    </main>
    <footer className="footer"><div className="container">Project 22 · UCI Wholesale Customers · K-Means phục vụ mô tả cơ cấu chi tiêu · Không sử dụng để đánh giá con người</div></footer>
  </div>;
}
