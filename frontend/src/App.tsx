import { useEffect, useRef, useState } from 'react';
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
type FinalProfile = {
  source_scope: 'train_plus_validation'; development_count: number; read_only: boolean; test_used: boolean;
  feature_columns: Feature[]; model_sha256: string; profiling_only_columns: ('Channel' | 'Region')[];
  cluster_summary: Profile[];
  cluster_sizes: { cluster_id: number; count: number; share: number }[];
  median_ratio: { cluster_id: number; values: Record<Feature, number> }[];
  channel_profile: { cluster_id: number; channel: number; count: number; within_cluster_share: number }[];
  region_profile: { cluster_id: number; region: number; count: number; within_cluster_share: number }[];
  distance_summary: {
    cluster_id: number; count: number; min: number; mean: number; median: number;
    p90: number; p95: number; max: number; q1: number; q3: number;
    iqr_upper_fence: number; iqr_distance_outlier_count: number; inertia_per_member: number;
  }[];
  outliers: { count: number; top_1pct_count: number; top_1pct_inertia_share: number; rule: string };
  inertia_per_row: number; distance_space: string; median_ratio_denominator: string;
  evidence_sha256: Record<string, string>;
};
type Dashboard = {
  selection_decision: string; k: number; preprocessing: string;
  final_profile: FinalProfile;
  experiments: Experiment[]; training: { rows: number; silhouette: number; inertia_per_row: number };
  final_test: { rows: number; silhouette: number; inertia_per_row: number; cluster_counts: Record<string, number> };
  profiles: Profile[]; metric_note: string;
};
const EXPERIMENT_K = [2, 3, 4, 5, 6, 7, 8] as const;
const CATEGORY_NAMES = {
  channel: { 1: 'Horeca', 2: 'Bán lẻ' },
  region: { 1: 'Lisbon', 2: 'Oporto', 3: 'Khu vực khác' },
} as const;
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

function verifyDashboard(payload: Dashboard): Dashboard {
  const final = payload?.final_profile;
  if (payload?.selection_decision !== 'D011' || payload.k !== 2 ||
      payload.preprocessing !== 'log1p_standardscaler' ||
      !Array.isArray(payload.experiments) || payload.experiments.length !== 14 ||
      !final || final.source_scope !== 'train_plus_validation' ||
      final.development_count !== 352 || final.read_only !== true || final.test_used !== false ||
      !Array.isArray(final.feature_columns) ||
      final.feature_columns.join(',') !== FIELDS.map(f => f.key).join(',') ||
      !Array.isArray(final.cluster_sizes) || final.cluster_sizes.length !== 2 ||
      final.cluster_sizes[0].cluster_id !== 0 || final.cluster_sizes[1].cluster_id !== 1 ||
      final.cluster_sizes[0].count + final.cluster_sizes[1].count !== 352 ||
      !Array.isArray(final.cluster_summary) || final.cluster_summary.length !== 2 ||
      !Array.isArray(final.median_ratio) || final.median_ratio.length !== 2 ||
      !Array.isArray(final.channel_profile) || final.channel_profile.length !== 4 ||
      !Array.isArray(final.region_profile) || final.region_profile.length !== 6 ||
      !Array.isArray(final.distance_summary) || final.distance_summary.length !== 2 ||
      !final.outliers || !Number.isFinite(final.outliers.count)) {
    throw new Error('Hồ sơ phân khúc cuối thiếu hoặc không hợp lệ.');
  }
  return payload;
}

function CandidateExplorer({ candidate, selectionK, preprocessing, valueK, onChangeK }: {
  candidate: Experiment | undefined; selectionK: number; preprocessing: string;
  valueK: number; onChangeK: (value: number) => void;
}) {
  return <section className="candidate-explorer" aria-label="Khám phá cấu hình K">
    <div className="section-heading">
      <h3>Khám phá cấu hình K</h3>
      <p>Chỉ xem bằng chứng train/validation; không thay đổi mô hình phân khúc cuối.</p>
    </div>
    <div className="candidate-k-controls" role="group" aria-label="Chọn K để xem thí nghiệm">
      {EXPERIMENT_K.map(k =>
        <button type="button" key={k} className={valueK === k ? 'toggle-selected' : ''}
          aria-pressed={valueK === k} onClick={() => onChangeK(k)}>K={k}</button>)}
    </div>
    {candidate ? <>
      <div className="candidate-heading"><strong>{preprocessing === 'raw' ? 'Raw' : 'Log1p + StandardScaler'} · K={candidate.k}</strong>
        {candidate.k === selectionK && preprocessing === 'log1p_standardscaler' &&
          <span className="candidate-frozen-note">D011 · Mô hình được chọn</span>}
      </div>
      <dl className="candidate-metrics">
        <div><dt>Train inertia</dt><dd data-testid="candidate-inertia">{formatNumber(candidate.train_inertia, 2)}</dd></div>
        <div><dt>Validation silhouette</dt><dd data-testid="candidate-silhouette">{formatNumber(candidate.validation_silhouette, 4)}</dd></div>
        <div><dt>ARI stability</dt><dd data-testid="candidate-ari">{formatNumber(candidate.ari, 4)}</dd></div>
        <div><dt>Tỷ trọng cụm nhỏ nhất</dt><dd data-testid="candidate-min-share">{formatPercent(candidate.min_cluster_share)}</dd></div>
      </dl>
    </> : <p className="notice notice-error" role="alert">Không có bằng chứng thí nghiệm cho lựa chọn này.</p>}
    <p className="muted small-note">K phục vụ luôn cố định: {selectionK}. Các candidate chỉ là kết quả thí nghiệm, không có hồ sơ 352 mẫu hay model serving riêng.</p>
  </section>;
}

function ClusterSizeChart({ profile }: { profile: FinalProfile }) {
  const ordered = [...profile.cluster_sizes].sort((a,b) => a.cluster_id - b.cluster_id);
  return <div className="analysis-block">
    <h3>Quy mô hai cụm</h3>
    <div className="cluster-size-track" role="img" aria-label={'Quy mô cụm: ' +
      ordered.map(r => 'cụm ' + r.cluster_id + ' ' + r.count + ' khách, ' + formatPercent(r.share)).join('; ')}>
      {ordered.map(row => <span key={row.cluster_id} className={'cluster-size-part cluster-color-' + row.cluster_id}
        style={{ width: (row.share * 100) + '%' }} />)}
    </div>
    <div className="cluster-size-legend">
      {ordered.map(row => <div key={row.cluster_id}>
        <span className={'cluster-dot cluster-color-' + row.cluster_id} />
        <strong>Cụm {row.cluster_id}: {formatNumber(row.count)} khách</strong>
        <span className="muted">{formatPercent(row.share)}</span>
      </div>)}
    </div>
    <p className="muted small-note">Tỷ trọng của 352 khách development, không phải số lượng khách mới được dự đoán.</p>
  </div>;
}

function MedianRatioChart({ profile }: { profile: FinalProfile }) {
  const ratios = [...profile.median_ratio].sort((a,b) => a.cluster_id - b.cluster_id);
  const max = Math.max(1, ...ratios.flatMap(r => FIELDS.map(f => r.values[f.key])));
  const reference = 100 / max;
  const description = 'Tỷ lệ median theo cụm so với median của toàn bộ 352 khách: ' +
    FIELDS.map(f => f.key + ' ' + ratios.map(r => 'cụm ' + r.cluster_id + ' ' +
      r.values[f.key].toFixed(3)).join(', ')).join('; ');
  return <div className="analysis-block">
    <h3>So sánh median chi tiêu</h3>
    <p className="muted small-note">Tỷ lệ so với median chung của 352 mẫu development; mốc 1,0 là bằng median chung. Các thanh dùng cùng thang đo.</p>
    <div className="ratio-legend"><span className="cluster-dot cluster-color-0"/> Cụm 0
      <span className="cluster-dot cluster-color-1"/> Cụm 1
      <span className="ratio-reference-symbol"/> Mốc 1,0</div>
    <div className="median-chart" role="img" aria-label={description}>
      {FIELDS.map(f => <div className="median-chart-row" key={f.key}>
        <strong>{f.label}</strong>
        <div className="median-series">
          {ratios.map(r => <div className="median-bar-row" key={r.cluster_id}>
            <div className="median-bar-track">
              <span className="median-reference-line" style={{ left: reference + '%' }}/>
              <span className={'median-bar cluster-color-' + r.cluster_id}
                style={{ width: (r.values[f.key] / max * 100) + '%' }}/>
            </div>
            <span className="median-value">{formatNumber(r.values[f.key], 2)}×</span>
          </div>)}
        </div>
      </div>)}
    </div>
    <p className="muted small-note">Chi tiêu gốc theo đơn vị monetary units của UCI; tỷ lệ trên không phải số tiền hay độ tin cậy.</p>
  </div>;
}

type DistributionRow = { cluster_id: number; count: number; within_cluster_share: number; channel?: number; region?: number };
function DistributionChart({ title, field, rows, sizes }: {
  title: string; field: 'channel' | 'region'; rows: DistributionRow[];
  sizes: FinalProfile['cluster_sizes'];
}) {
  const codes = field === 'channel' ? [1,2] : [1,2,3];
  const categories = CATEGORY_NAMES[field];
  return <section className="analysis-block distribution-chart">
    <h3>{title}</h3>
    <p className="muted small-note">Tỷ lệ theo từng cụm, chỉ dùng để diễn giải hậu phân cụm, không tham gia huấn luyện hoặc chọn K.</p>
    <div className="category-legend">
      {codes.map(code => <span key={code}><span className={'category-dot category-' + code}/>{categories[code as keyof typeof categories]} ({code})</span>)}
    </div>
    {sizes.map(c => {
      const details = codes.map(code => rows.find(r => r.cluster_id === c.cluster_id &&
        (field === 'channel' ? r.channel : r.region) === code));
      return <div className="category-cluster" key={c.cluster_id}>
        <div className="category-heading"><strong>Cụm {c.cluster_id}</strong><span className="muted">{c.count} khách</span></div>
        <div role="img" className="category-track" aria-label={title + ', cụm ' + c.cluster_id + ': ' +
          details.map((row,i) => String(categories[codes[i] as keyof typeof categories]) +
            ' ' + (row?.count ?? 0) + ' khách, ' + formatPercent(row?.within_cluster_share ?? 0)).join('; ')}>
          {details.map((row,i) => <span key={codes[i]} className={'category-segment category-' + codes[i]}
            style={{ width: ((row?.within_cluster_share ?? 0) * 100) + '%' }} />)}
        </div>
      </div>;
    })}
    <div className="table-scroll">
      <table className="data-table">
        <caption className="sr-only">{title} theo số lượng và tỷ trọng từng cụm</caption>
        <thead><tr><th scope="col">Cụm</th><th scope="col">{field === 'channel' ? 'Channel' : 'Region'}</th><th scope="col">Khách</th><th scope="col">Trong cụm</th></tr></thead>
        <tbody>{rows.map(row => {
          const code = field === 'channel' ? row.channel : row.region;
          return <tr key={row.cluster_id + '-' + code}><th scope="row">Cụm {row.cluster_id}</th>
            <td>{categories[code as keyof typeof categories]} ({code})</td>
            <td>{formatNumber(row.count)}</td><td>{formatPercent(row.within_cluster_share)}</td></tr>;
        })}</tbody>
      </table>
    </div>
  </section>;
}

function DistanceChart({ profile }: { profile: FinalProfile }) {
  const distances = [...profile.distance_summary].sort((a,b) => a.cluster_id - b.cluster_id);
  const max = Math.max(1, ...distances.map(r => r.max));
  return <section className="analysis-block">
    <h3>Khoảng cách tới tâm cụm</h3>
    <p className="muted small-note">Khoảng cách Euclidean trong không gian log1p + StandardScaler; không phải xác suất hay độ tin cậy.</p>
    <div className="ratio-legend"><span className="cluster-dot cluster-color-0" /> P95
      <span className="distance-max-symbol" /> Khoảng cách lớn nhất</div>
    <div className="distance-chart" role="img" aria-label={'Khoảng cách tới tâm cụm: ' +
      distances.map(d => 'cụm ' + d.cluster_id + ' trung vị ' + d.median.toFixed(3) +
        ', P95 ' + d.p95.toFixed(3) + ', tối đa ' + d.max.toFixed(3) +
        ', ngoại lệ IQR ' + d.iqr_distance_outlier_count).join('; ')}>
      {distances.map(d => <div className="distance-chart-row" key={d.cluster_id}>
        <strong>Cụm {d.cluster_id}</strong><div className="distance-track">
          <span className="distance-maximum" style={{ width: (d.max / max * 100) + '%' }}/>
          <span className="distance-p95" style={{ width: (d.p95 / max * 100) + '%' }}/>
        </div><span className="distance-label">P95 {formatNumber(d.p95, 2)}</span>
      </div>)}
    </div>
    <div className="table-scroll">
      <table className="data-table">
        <caption className="sr-only">Thống kê khoảng cách của mô hình cuối</caption>
        <thead><tr><th scope="col">Cụm</th><th scope="col">Trung vị</th><th scope="col">P95</th><th scope="col">Tối đa</th><th scope="col">Ngoại lệ IQR</th></tr></thead>
        <tbody>{distances.map(d => <tr key={d.cluster_id}>
          <th scope="row">Cụm {d.cluster_id}</th><td>{formatNumber(d.median, 3)}</td>
          <td>{formatNumber(d.p95, 3)}</td><td>{formatNumber(d.max, 3)}</td>
          <td>{formatNumber(d.iqr_distance_outlier_count)}</td>
        </tr>)}</tbody>
      </table>
    </div>
    <p className="muted small-note">Tổng {formatNumber(profile.outliers.count)} mẫu ngoài ngưỡng khoảng cách Q3 + 1,5×IQR theo từng cụm; chỉ gắn cờ, không loại dữ liệu.</p>
  </section>;
}

export default function App() {
  const [screen, setScreen] = useState<Screen>('intro');
  const [info, setInfo] = useState<ModelInfo | null>(null);
  const [modelError, setModelError] = useState<string | null>(null);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [dashboardError, setDashboardError] = useState<string | null>(null);
  const [preprocessing, setPreprocessing] = useState('log1p_standardscaler');
  const [candidateK, setCandidateK] = useState<number>(2);
  const [values, setValues] = useState<Record<Feature, string>>({
    Fresh: '', Milk: '', Grocery: '', Frozen: '', Detergents_Paper: '', Delicassen: '',
  });
  const [result, setResult] = useState<SegmentResult | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const requestVersion = useRef(0);
  const clearPendingResult = () => {
    requestVersion.current += 1;
    setResult(null);
    setSubmitError(null);
    setSubmitting(false);
  };

  useEffect(() => {
    getJson<ModelInfo>('/api/model-info').then(setInfo).catch(e => setModelError(String(e.message)));
  }, []);
  useEffect(() => {
    if (screen !== 'dashboard' || dashboard) return;
    getJson<Dashboard>('/api/dashboard').then(verifyDashboard).then(setDashboard).catch(e => setDashboardError(String(e.message)));
  }, [screen, dashboard]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    clearPendingResult();
    const version = requestVersion.current;
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
      if (version === requestVersion.current) setResult(body);
    } catch(e) {
      if (version === requestVersion.current) setSubmitError(e instanceof Error ? e.message : 'Không thể phân khúc');
    } finally {
      if (version === requestVersion.current) setSubmitting(false);
    }
  };

  const filledExample = (profile: Profile) => {
    clearPendingResult();
    setValues(Object.fromEntries(FIELDS.map(f => [f.key, String(profile.median_spending[f.key])])) as Record<Feature, string>);
  };
  const allRows = dashboard?.experiments.filter(row => row.preprocessing === preprocessing) || [];
  const candidate = allRows.find(row => row.k === candidateK);

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
                onChange={event => { clearPendingResult(); setValues(prev => ({ ...prev, [f.key]: event.target.value })); }} />
              <small>{info?.reference_ranges?.[f.key] ? 'Train quan sát: ' + formatNumber(info.reference_ranges[f.key].min) + ' – ' + formatNumber(info.reference_ranges[f.key].max) : 'Giá trị không âm'}</small>
            </label>)}</div>
            {submitError && <p className="notice notice-error" role="alert">{submitError}</p>}
            <div className="form-footer"><button className="btn-primary" type="submit" disabled={submitting || !info}>{submitting ? 'Đang xử lý…' : 'Phân khúc khách hàng'}</button><button className="btn-subtle" type="button" onClick={() => { clearPendingResult(); setValues({ Fresh:'', Milk:'', Grocery:'', Frozen:'', Detergents_Paper:'', Delicassen:'' }); }}>Xóa dữ liệu</button></div>
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
            <CandidateExplorer candidate={candidate} selectionK={dashboard.k} preprocessing={preprocessing}
              valueK={candidateK} onChangeK={setCandidateK}/>
            <p className="muted small-note">{dashboard.metric_note}</p>
          </section>
          <section className="content-card" aria-label="Hồ sơ phân khúc cuối">
            <div className="section-heading"><h2>Hồ sơ 2 phân khúc cuối</h2>
              <p>Model D011 K=2; hậu phân cụm trên {dashboard.final_profile.development_count} khách train + validation, không sử dụng tập test.</p>
            </div>
            <ClusterSizeChart profile={dashboard.final_profile}/>
            <div className="profile-analysis-grid">
              <MedianRatioChart profile={dashboard.final_profile}/>
              <DistanceChart profile={dashboard.final_profile}/>
            </div>
            <div className="profile-analysis-grid">
              <DistributionChart title="Phân bố Channel" field="channel" rows={dashboard.final_profile.channel_profile}
                sizes={dashboard.final_profile.cluster_sizes}/>
              <DistributionChart title="Phân bố Region" field="region" rows={dashboard.final_profile.region_profile}
                sizes={dashboard.final_profile.cluster_sizes}/>
            </div>
            <div className="section-heading profile-detail-heading"><h3>Median chi tiêu gốc theo cụm</h3>
              <p>Đơn vị chi tiêu theo dữ liệu UCI Wholesale Customers; số liệu trích từ model đã đóng băng.</p></div>
            <div className="profile-grid">{dashboard.final_profile.cluster_summary.map(p => <ProfileCard key={p.cluster_id} profile={p} />)}</div>
          </section>
          <section className="content-card"><div className="section-heading"><h2>Model card</h2><p>Trạng thái mô hình đã freeze trước final test.</p></div>
            <dl className="model-facts"><div><dt>Preprocessing</dt><dd>log1p + StandardScaler</dd></div><div><dt>Số cụm</dt><dd>2</dd></div><div><dt>Huấn luyện</dt><dd>{dashboard.final_profile.development_count} khách (train + validation)</dd></div><div><dt>Final test</dt><dd>88 khách, silhouette {formatNumber(dashboard.final_test.silhouette, 6)}</dd></div><div><dt>Artifact SHA-256</dt><dd className="hash">{dashboard.final_profile.model_sha256}</dd></div>
              <div><dt>Phạm vi profiling</dt><dd>Development 352 · Channel/Region chỉ diễn giải</dd></div>
              <div><dt>Hồ sơ kiểm chứng</dt><dd>{Object.keys(dashboard.final_profile.evidence_sha256).length} CSV đã xác minh SHA-256 tại Backend</dd></div></dl>
            <p className="muted small-note">{info?.limitations}</p>
          </section>
        </>}
      </section>}
    </main>
    <footer className="footer"><div className="container">Project 22 · UCI Wholesale Customers · K-Means phục vụ mô tả cơ cấu chi tiêu · Không sử dụng để đánh giá con người</div></footer>
  </div>;
}
