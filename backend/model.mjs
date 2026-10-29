import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { loadVerifiedFinalProfile } from './final-profile.mjs';

export const FEATURES = Object.freeze(['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']);
const artifact = (name) => fileURLToPath(new URL('../' + name, import.meta.url));
const DIAGNOSTIC_POLICY = Object.freeze({
  nearBoundaryRelativeMargin: 0.10,
  highDistanceRatioToDevelopmentRms: 1.5,
});
function buildDecisionSupport({ nearBoundary, highDistance, outOfRangeFeatures, distanceRatio }) {
  const reasons = [];
  if (outOfRangeFeatures.length > 0) reasons.push('out_of_train_range');
  if (nearBoundary) reasons.push('near_boundary');
  if (highDistance) reasons.push('high_distance');
  if (reasons.length === 0) return {
    status: 'descriptive', priority: 'low', reason_codes: [],
    title: 'Có thể dùng để mô tả cơ cấu chi tiêu',
    action: 'Đọc median của cụm được gán như một mô tả khuynh hướng, không suy ra giá trị kinh doanh của khách.',
    rationale: 'Điểm nằm trong khoảng tham chiếu theo từng biến, đủ xa biên giữa hai tâm và không vượt ngưỡng khoảng cách rà soát.',
  };
  if (outOfRangeFeatures.length > 0 && highDistance) return {
    status: 'review', priority: 'high', reason_codes: reasons,
    title: 'Cần rà soát dữ liệu trước khi diễn giải',
    action: 'Xác minh đơn vị, kỳ chi tiêu và các biến ngoài khoảng train; sau đó xem cả median cụm được gán lẫn cụm còn lại.',
    rationale: 'Đầu vào vừa nằm ngoài miền quan sát của train vừa cách xa các hồ sơ development, nên nhãn gần nhất chỉ nên xem là tham khảo.',
  };
  if (outOfRangeFeatures.length > 0) return {
    status: 'review', priority: 'medium', reason_codes: reasons,
    title: 'Đầu vào có biến ngoài khoảng quan sát',
    action: 'Xác minh đơn vị và kỳ chi tiêu của biến được cảnh báo; không tự động cắt ngưỡng hoặc quy đổi giá trị.',
    rationale: 'Mô hình vẫn trả nhãn gần nhất nhưng dữ liệu này khác miền min/max của 264 mẫu train ở bước EDA.',
  };
  if (nearBoundary) return {
    status: 'review', priority: 'medium', reason_codes: reasons,
    title: 'Điểm nằm gần biên giữa hai cụm',
    action: 'Xem đồng thời median của hai cụm và tránh diễn giải đây là một phân loại chắc chắn.',
    rationale: 'Khoảng cách tới hai centroid gần nhau; mã cụm được trả theo quy tắc tâm gần nhất, không phải xác suất thuộc cụm.',
  };
  return {
    status: 'review', priority: 'medium', reason_codes: reasons,
    title: 'Điểm cách xa hồ sơ development',
    action: 'Rà soát các khoản chi tiêu cực trị và dùng kết quả như tín hiệu khám phá, không dùng để tự động quyết định phục vụ.',
    rationale: 'Khoảng cách tới tâm được gán vượt ngưỡng rà soát ' + distanceRatio.toFixed(2) + '× RMS development.',
  };
}


function readJson(path) { return JSON.parse(readFileSync(path, 'utf8')); }
function sameArray(a, b) { return Array.isArray(a) && a.length === b.length && a.every((v, i) => v === b[i]); }
function finiteArray(a, n) { return Array.isArray(a) && a.length === n && a.every(v => typeof v === 'number' && Number.isFinite(v)); }
function verifyModel(model, frozen, evaluation) {
  if (model.schema_version !== 1 || model.selection_decision !== 'D011' || model.preprocessing !== 'log1p_standardscaler' ||
      model.k !== 2 || model.training_count !== 352 || model.training_scope !== 'train_plus_validation' ||
      model.test_used_for_training !== false || !sameArray(model.feature_columns, FEATURES) ||
      frozen.status !== 'FROZEN' || frozen.k !== model.k || frozen.preprocessing !== model.preprocessing ||
      !sameArray(frozen.feature_columns, FEATURES) ||
      evaluation.status !== 'COMPLETE' || evaluation.test_used_for_selection !== false ||
      evaluation.selection_unchanged_after_test !== true) throw new Error('Gate 5 metadata does not match the frozen D011 model');
  if (!finiteArray(model.scaler_mean, 6) || !finiteArray(model.scaler_scale, 6) ||
      model.scaler_scale.some(v => v <= 0) ||
      !Array.isArray(model.cluster_centers) || model.cluster_centers.length !== 2 ||
      !model.cluster_centers.every(c => finiteArray(c, 6)) ||
      !Array.isArray(model.cluster_profiles) || model.cluster_profiles.length !== 2 ||
      !model.cluster_profiles.every((p, i) => p.cluster === i && typeof p.profile_name === 'string' &&
        p.profile_name.length > 0 && FEATURES.every(f => Number.isFinite(p.median_spending?.[f])))) {
    throw new Error('Invalid frozen model schema');
  }
}
function readRanges() {
  const csv = readFileSync(artifact('reports/data/eda/train_summary_raw.csv'), 'utf8').trim().split(/\r?\n/);
  const columns = csv[0].split(',');
  const minAt = columns.indexOf('min'), maxAt = columns.indexOf('max'), featureAt = columns.indexOf('feature');
  if (minAt < 0 || maxAt < 0 || featureAt < 0) throw new Error('Invalid EDA range CSV schema');
  const ranges = Object.fromEntries(csv.slice(1).map(row => {
    const values = row.split(',');
    return [values[featureAt], { min: Number(values[minAt]), max: Number(values[maxAt]) }];
  }));
  if (!FEATURES.every(f => Number.isFinite(ranges[f]?.min) && Number.isFinite(ranges[f]?.max))) throw new Error('Incomplete EDA ranges');
  return ranges;
}
export function loadModel({ modelPath = artifact('models/model.json') } = {}) {
  const raw = readFileSync(modelPath);
  const evaluation = readJson(artifact('models/final_evaluation.json'));
  const bytesSha = createHash('sha256').update(raw).digest('hex');
  // Gate 5 computed the checksum on Windows CRLF bytes; Git may check out LF on Linux.
  // Accept only a byte-identical file or the exact same content with canonical CRLF line endings.
  const crlfSha = createHash('sha256').update(raw.toString('utf8').replace(/\r?\n/g, '\r\n')).digest('hex');
  if (bytesSha !== evaluation.model_json_sha256 && crlfSha !== evaluation.model_json_sha256) {
    throw new Error('Frozen model checksum mismatch');
  }
  const checksum = evaluation.model_json_sha256;
  const model = JSON.parse(raw.toString('utf8'));
  const selection = readJson(artifact('models/selection.json'));
  verifyModel(model, selection, evaluation);
  return Object.freeze({ model, evaluation, checksum, ranges: readRanges() });
}
export function segment(loaded, spending) {
  const { model, evaluation, ranges } = loaded;
  if (!spending || typeof spending !== 'object' || Array.isArray(spending) ||
    Object.keys(spending).length !== FEATURES.length ||
    !FEATURES.every(f => Object.hasOwn(spending, f) && typeof spending[f] === 'number' &&
      Number.isFinite(spending[f]) && spending[f] >= 0)) throw new TypeError('Six finite nonnegative spending values are required');
  const scaled = FEATURES.map((f, i) => (Math.log1p(spending[f]) - model.scaler_mean[i]) / model.scaler_scale[i]);
  const distances = model.cluster_centers.map(center => Math.sqrt(
    scaled.reduce((sum, v, i) => sum + (v - center[i]) ** 2, 0)
  ));
  const cluster = distances[1] < distances[0] ? 1 : 0; // sklearn: first center wins ties
  const alternativeCluster = 1 - cluster;
  const profile = model.cluster_profiles[cluster];
  const alternativeProfile = model.cluster_profiles[alternativeCluster];
  const distance = distances[cluster];
  const alternativeDistance = distances[alternativeCluster];
  const distanceGap = alternativeDistance - distance;
  const relativeMargin = distanceGap / Math.max(alternativeDistance, Number.EPSILON);
  const developmentRms = Math.sqrt(evaluation.training.inertia_per_row);
  const distanceRatio = distance / developmentRms;
  const outOfTrainRangeFeatures = FEATURES.filter(f => spending[f] < ranges[f].min || spending[f] > ranges[f].max);
  const warnings = outOfTrainRangeFeatures.map(f =>
    f + ': ngoài khoảng quan sát của train (264 khách), kết quả cần thận trọng');
  const nearBoundary = relativeMargin < DIAGNOSTIC_POLICY.nearBoundaryRelativeMargin;
  const highDistance = distanceRatio > DIAGNOSTIC_POLICY.highDistanceRatioToDevelopmentRms;
  return {
    cluster_id: cluster,
    distance_to_centroid: distance,
    distances_to_centroids: distances,
    distance_gap: distanceGap,
    relative_margin: relativeMargin,
    distance_ratio_to_development_rms: distanceRatio,
    out_of_train_range_features: outOfTrainRangeFeatures,
    profile: { name: profile.profile_name, count: profile.count, share: profile.share, median_spending: profile.median_spending },
    alternative_profile: { name: alternativeProfile.profile_name, count: alternativeProfile.count, share: alternativeProfile.share, median_spending: alternativeProfile.median_spending },
    warnings,
    decision_support: buildDecisionSupport({
      nearBoundary,
      highDistance,
      outOfRangeFeatures: outOfTrainRangeFeatures,
      distanceRatio,
    }),
    distance_space: 'log1p + StandardScaler (Euclidean)',
  };
}
export function modelInfo(loaded) {
  const m = loaded.model;
  return {
    status: 'ready', selection_decision: m.selection_decision, preprocessing: m.preprocessing,
    k: m.k, feature_columns: m.feature_columns, training_count: m.training_count,
    training_scope: m.training_scope, random_state: m.random_state,
    artifact_sha256: loaded.checksum,
    profiles: m.cluster_profiles.map(p => ({ cluster_id: p.cluster, name: p.profile_name, count: p.count, share: p.share, median_spending: p.median_spending })),
    reference_ranges: loaded.ranges,
    diagnostic_policy: {
      near_boundary_relative_margin: DIAGNOSTIC_POLICY.nearBoundaryRelativeMargin,
      high_distance_ratio_to_development_rms: DIAGNOSTIC_POLICY.highDistanceRatioToDevelopmentRms,
      development_rms_distance: Math.sqrt(loaded.evaluation.training.inertia_per_row),
      note: 'Đây là ngưỡng rà soát mô tả; không phải xác suất, confidence hay nhãn mới.',
    },
    data_card: {
      dataset: 'Wholesale customers',
      uci_id: 292,
      source_url: 'https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers',
      doi: 'https://doi.org/10.24432/C5030X',
      license: 'CC BY 4.0',
      row_count: 440,
      spending_period: 'annual',
      spending_unit: 'monetary units (m.u.)',
      currency_known: false,
      feature_columns: [...FEATURES],
      profiling_only_columns: ['Channel', 'Region'],
      data_available_when: 'Đã ghi nhận đầy đủ chi tiêu hằng năm của khách ở cả sáu nhóm hàng; không phải dự báo cho khách chưa có lịch sử.',
      source_policy: 'Dữ liệu UCI lịch sử; chưa có kiểm chứng hiệu quả với khách hàng thực tế mới.',
    },
    model_card: {
      decision: m.selection_decision,
      algorithm: 'KMeans (' + m.algorithm + ')',
      random_state: m.random_state, n_init: m.n_init, max_iter: m.max_iter,
      preprocessing: m.preprocessing, k: m.k,
      selection_scope: 'train + validation only; before independent final test',
      fit_scope: m.training_scope,
      fit_rows: m.training_count,
      held_out_test_rows: loaded.evaluation.final_test.rows,
      held_out_test_evaluated_once: loaded.evaluation.test_evaluated_once,
      cluster_labels: 'Tên mô tả dựa trên median development; cluster ID không có thứ bậc.',
      selection_rationale: 'D011 chọn Log1p + StandardScaler và K=2 nhờ độ ổn định giữa các seed, tỷ trọng cụm cân bằng và hồ sơ hai nhóm giữ xu hướng sau refit trên 352 mẫu. Raw K=2 có silhouette cao hơn nhưng chịu ảnh hưởng nhiều hơn bởi điểm xa; K=3 mất ổn định về hồ sơ sau refit.',
      assumptions: 'K-Means dùng khoảng cách Euclidean trong không gian đã chuẩn hóa, ưu tiên các cụm tương đối gọn; nhạy cảm với outlier và preprocessing.',
      intended_use: 'Khám phá cơ cấu chi tiêu, mô tả hai nhóm và thảo luận chiến lược phục vụ trên dữ liệu tương tự.',
      prohibited_inferences: 'Không dùng cụm để khẳng định doanh thu, lợi nhuận, chất lượng, rủi ro hay giá trị của cá nhân; không dùng làm cơ sở từ chối khách.',
      metric_cautions: 'Silhouette đo phân tách cụm, ARI so sánh phân hoạch qua seed; không có nhãn thật để tính accuracy. Inertia raw và scaled không có cùng thang đo.',
      distance_cautions: 'Khoảng cách tâm cụm không phải xác suất/độ tin cậy; cờ ngoài khoảng train chỉ xét từng biến so với 264 mẫu EDA, khác ngoại lệ IQR khoảng cách của 352 development.',
    },
    reference_note: 'Khoảng min/max chỉ dựa trên 264 mẫu train ở bước EDA; vượt khoảng này là cảnh báo, không bị tự thay đổi.',
    limitations: 'Phân cụm không có nhãn thật hay xác suất dự đoán; khoảng cách không phải độ tin cậy và không chứng minh giá trị khách hàng.',
  };
}
export function dashboard(loaded, { profileDir } = {}) {
  const source = readFileSync(artifact('reports/data/experiments/selection_evidence.csv'), 'utf8').trim().split(/\r?\n/);
  const columns = source[0].split(',');
  const required = ['preprocessing', 'k', 'train_inertia_mean', 'validation_silhouette_mean', 'validation_silhouette_std', 'ari_mean', 'ari_min', 'ari_max', 'pair_count', 'min_cluster_share_mean'];
  if (!required.every(key => columns.includes(key))) throw new Error('Experiment evidence missing columns');
  const experiments = source.slice(1).filter(Boolean).map(line => {
    const cells = line.split(',');
    const row = Object.fromEntries(columns.map((col, index) => [col, cells[index]]));
    return { preprocessing: row.preprocessing, k: Number(row.k), train_inertia: Number(row.train_inertia_mean),
      validation_silhouette: Number(row.validation_silhouette_mean), validation_silhouette_std: Number(row.validation_silhouette_std),
      ari: Number(row.ari_mean), ari_min: Number(row.ari_min), ari_max: Number(row.ari_max),
      pair_count: Number(row.pair_count), min_cluster_share: Number(row.min_cluster_share_mean) };
  });
  if (experiments.length !== 14 || experiments.some(x => !['raw','log1p_standardscaler'].includes(x.preprocessing) ||
      !Number.isInteger(x.k) || x.k < 2 || x.k > 8 ||
      ![x.train_inertia, x.validation_silhouette, x.validation_silhouette_std, x.ari, x.ari_min, x.ari_max, x.min_cluster_share].every(Number.isFinite) ||
      x.pair_count !== 45 || x.ari_min > x.ari || x.ari > x.ari_max)) {
    throw new Error('Invalid frozen experiment evidence');
  }
  return {
    selection_decision: 'D011', k: loaded.model.k, preprocessing: loaded.model.preprocessing,
    experiments,
    training: loaded.evaluation.training,
    final_test: loaded.evaluation.final_test,
    profiles: modelInfo(loaded).profiles,
    final_profile: loadVerifiedFinalProfile(loaded, { profileDir }),
    metric_note: 'Elbow/inertia chỉ so sánh trong cùng không gian preprocessing. Test đã đánh giá một lần, không sử dụng để chọn K.',
  };
}
