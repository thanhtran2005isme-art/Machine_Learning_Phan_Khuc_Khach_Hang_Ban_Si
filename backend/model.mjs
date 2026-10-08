import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { loadVerifiedFinalProfile } from './final-profile.mjs';

export const FEATURES = Object.freeze(['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']);
const artifact = (name) => fileURLToPath(new URL('../' + name, import.meta.url));

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
  const { model, ranges } = loaded;
  if (!spending || typeof spending !== 'object' || Array.isArray(spending) ||
    Object.keys(spending).length !== FEATURES.length ||
    !FEATURES.every(f => Object.hasOwn(spending, f) && typeof spending[f] === 'number' &&
      Number.isFinite(spending[f]) && spending[f] >= 0)) throw new TypeError('Six finite nonnegative spending values are required');
  const scaled = FEATURES.map((f, i) => (Math.log1p(spending[f]) - model.scaler_mean[i]) / model.scaler_scale[i]);
  const distances = model.cluster_centers.map(center => Math.sqrt(
    scaled.reduce((sum, v, i) => sum + (v - center[i]) ** 2, 0)
  ));
  const cluster = distances[1] < distances[0] ? 1 : 0; // sklearn: first center wins ties
  const profile = model.cluster_profiles[cluster];
  const warnings = FEATURES.flatMap(f => spending[f] < ranges[f].min || spending[f] > ranges[f].max
    ? [f + ': ngoài khoảng quan sát của train (264 khách), kết quả cần thận trọng'] : []);
  return {
    cluster_id: cluster,
    distance_to_centroid: distances[cluster],
    distances_to_centroids: distances,
    profile: { name: profile.profile_name, count: profile.count, share: profile.share, median_spending: profile.median_spending },
    warnings,
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
    reference_note: 'Khoảng min/max chỉ dựa trên 264 mẫu train ở bước EDA; vượt khoảng này là cảnh báo, không bị tự thay đổi.',
    limitations: 'Phân cụm không có nhãn thật hay xác suất dự đoán; khoảng cách không phải độ tin cậy và không chứng minh giá trị khách hàng.',
  };
}
export function dashboard(loaded, { profileDir } = {}) {
  const source = readFileSync(artifact('reports/data/experiments/selection_evidence.csv'), 'utf8').trim().split(/\r?\n/);
  const columns = source[0].split(',');
  const required = ['preprocessing', 'k', 'train_inertia_mean', 'validation_silhouette_mean', 'ari_mean', 'min_cluster_share_mean'];
  if (!required.every(key => columns.includes(key))) throw new Error('Experiment evidence missing columns');
  const experiments = source.slice(1).filter(Boolean).map(line => {
    const cells = line.split(',');
    const row = Object.fromEntries(columns.map((col, index) => [col, cells[index]]));
    return { preprocessing: row.preprocessing, k: Number(row.k), train_inertia: Number(row.train_inertia_mean),
      validation_silhouette: Number(row.validation_silhouette_mean), ari: Number(row.ari_mean), min_cluster_share: Number(row.min_cluster_share_mean) };
  });
  if (experiments.length !== 14 || experiments.some(x => !['raw','log1p_standardscaler'].includes(x.preprocessing) ||
      !Number.isInteger(x.k) || x.k < 2 || x.k > 8 ||
      ![x.train_inertia, x.validation_silhouette, x.ari, x.min_cluster_share].every(Number.isFinite))) {
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
