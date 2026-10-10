import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const DEFAULT_DIR = fileURLToPath(new URL('../reports/data/development_extension/', import.meta.url));
const FEATURES = ['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen'];
const HEX_SHA = /^[a-f0-9]{64}$/;
const need = (condition, message) => {
  if (!condition) throw new Error('Gate10.2 extension invalid: ' + message);
};
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x);
const finite = x => typeof x === 'number' && Number.isFinite(x);
const arrayEq = (a,b) => Array.isArray(a) && a.length===b.length && a.every((x,i)=>x===b[i]);
const close = (a,b,tol=1e-9) => finite(a)&&finite(b) && Math.abs(a-b)<=tol;
const sha = raw => createHash('sha256').update(raw).digest('hex');
const choose = n => n*(n-1)/2;

export function loadVerifiedDevelopmentExtension(loaded, { extensionDir = DEFAULT_DIR } = {}) {
  need(object(loaded) && object(loaded.model) && object(loaded.evaluation), 'frozen model missing');
  const m = loaded.model, e = loaded.evaluation;
  const meta = JSON.parse(readFileSync(join(extensionDir, 'metadata.json'), 'utf8'));
  need(meta.schema_version === 1 && meta.status === 'COMPLETE' &&
    meta.scope === 'train_plus_validation' && meta.decision === 'D011' &&
    meta.development_count === 352 && m.training_count === 352 && m.k === 2 &&
    meta.source_rows?.train === 264 && meta.source_rows?.validation === 88 &&
    arrayEq(meta.feature_columns, FEATURES) &&
    arrayEq(meta.profiling_only_columns, ['Channel','Region']) &&
    meta.frozen_model_fit_performed === false && meta.frozen_scaler_fit_performed === false &&
    meta.pca_fit_performed === true && meta.hierarchical_fit_performed === true &&
    meta.test_used === false && meta.test_evaluated === false &&
    meta.serving_model_changed === false &&
    meta.provenance?.model_sha256 === loaded.checksum &&
    meta.provenance?.selection_sha256 === e.selection_sha256 &&
    meta.provenance?.train_sha256 && HEX_SHA.test(meta.provenance.train_sha256) &&
    meta.provenance?.validation_sha256 && HEX_SHA.test(meta.provenance.validation_sha256) &&
    object(meta.files) && Object.keys(meta.files).length === 1 &&
    meta.files['analysis.json']?.path === 'reports/data/development_extension/analysis.json' &&
    HEX_SHA.test(meta.files['analysis.json'].sha256), 'metadata/provenance mismatch');

  const raw = readFileSync(join(extensionDir, 'analysis.json'));
  const canonical = raw.toString('utf8').replace(/\r\n/g,'\n');
  need(sha(raw)===meta.files['analysis.json'].sha256 ||
    sha(Buffer.from(canonical,'utf8'))===meta.files['analysis.json'].sha256, 'SHA256 mismatch');
  const analysis = JSON.parse(canonical);
  need(analysis.schema_version === 1 && analysis.decision === 'D011' &&
    analysis.source_scope === 'train_plus_validation' &&
    analysis.feature_space === 'frozen log1p + StandardScaler (6 dimensions)' &&
    Array.isArray(analysis.points) && analysis.points.length === 352,
    'analysis scope/count');

  const projection = analysis.pca;
  need(object(projection) &&
    projection.method === 'PCA(n_components=2, svd_solver=full) fitted on 352 development' &&
    Array.isArray(projection.explained_variance_ratio) &&
    projection.explained_variance_ratio.length===2 &&
    projection.explained_variance_ratio.every(v=>finite(v)&&v>0&&v<1) &&
    projection.explained_variance_ratio.reduce((a,b)=>a+b,0) <= 1 + 1e-9 &&
    Array.isArray(projection.components) && projection.components.length===2 &&
    projection.components.every(c=>Array.isArray(c)&&c.length===6&&c.every(finite)),
    'PCA dimensions/variance');
  for (const c of projection.components) {
    need(close(c.reduce((s,v)=>s+v*v,0),1,1e-8), 'PCA component norm');
  }
  need(close(projection.components[0].reduce((s,v,i)=>s+v*projection.components[1][i],0),0,1e-8),
    'PCA components not orthogonal');

  const countsK=[0,0],countsH=[0,0],cross=[[0,0],[0,0]];
  let sumX=0,sumY=0;
  const ids=new Set();
  for (let i=0;i<analysis.points.length;i++){
    const p=analysis.points[i];
    need(object(p) && Object.keys(p).length===6 &&
      Number.isInteger(p.index) && p.index===i && !ids.has(i) &&
      p.split === (i<264?'train':'validation') &&
      finite(p.pc1) && finite(p.pc2) &&
      (p.kmeans===0 || p.kmeans===1) &&
      (p.hierarchical===0 || p.hierarchical===1),
      'row schema/index/split invalid at '+i);
    ids.add(i);sumX+=p.pc1;sumY+=p.pc2;
    countsK[p.kmeans]++; countsH[p.hierarchical]++;
    cross[p.kmeans][p.hierarchical]++;
  }
  need(Math.abs(sumX/352)<1e-8 && Math.abs(sumY/352)<1e-8, 'PCA projection must be centered');
  need(arrayEq(countsK, m.cluster_profiles.map(p=>p.count)) &&
    arrayEq(countsK,[162,190]) &&
    countsH[0]>0 && countsH[1]>0, 'cluster sizes/frozen labels');

  const cmp=analysis.comparison;
  need(object(cmp) && cmp.method==='AgglomerativeClustering' &&
    cmp.linkage==='ward' && cmp.metric==='euclidean' &&
    cmp.n_clusters===2 && cmp.fit_space==='frozen 6D log1p+StandardScaler' &&
    arrayEq(cmp.frozen_counts,countsK) && arrayEq(cmp.hierarchical_counts,countsH) &&
    Array.isArray(cmp.contingency) &&
    cross.every((row,i)=>arrayEq(cmp.contingency[i],row)) &&
    close(cmp.silhouette_kmeans,e.training.silhouette,1e-8) &&
    finite(cmp.silhouette_hierarchical) && cmp.silhouette_hierarchical>=-1 &&
    cmp.silhouette_hierarchical<=1 && finite(cmp.ari) &&
    cmp.ari>=-1 && cmp.ari<=1, 'comparison metadata/counts/metrics');
  const overlap=cross.flat().reduce((s,n)=>s+choose(n),0);
  const rowSum=countsK.reduce((s,n)=>s+choose(n),0);
  const colSum=countsH.reduce((s,n)=>s+choose(n),0);
  const expected=rowSum*colSum/choose(352);
  const denom=(rowSum+colSum)/2-expected;
  const ari=denom===0?1:(overlap-expected)/denom;
  need(close(cmp.ari,ari,1e-10), 'ARI inconsistent with contingency');

  return Object.freeze({
    ...analysis,
    evidence_sha256: meta.files['analysis.json'].sha256,
    model_sha256: loaded.checksum,
    development_count:352, test_used:false, read_only:true,
  });
}
