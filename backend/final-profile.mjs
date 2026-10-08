import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const DEFAULT_DIR = fileURLToPath(new URL('../reports/data/final_profile/', import.meta.url));
const FEATURES = Object.freeze(['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']);
const EXPECTED = Object.freeze({
  'cluster_summary.csv': ['cluster', 'profile_name', 'count', 'share', ...FEATURES],
  'median_ratio.csv': ['cluster', ...FEATURES],
  'cluster_sizes.csv': ['cluster', 'count', 'share'],
  'channel_profile.csv': ['cluster', 'Channel', 'count', 'within_cluster_share'],
  'region_profile.csv': ['cluster', 'Region', 'count', 'within_cluster_share'],
  'distance_summary.csv': ['cluster', 'count', 'min', 'mean', 'median', 'p90', 'p95', 'max',
    'q1', 'q3', 'iqr_upper_fence', 'iqr_distance_outlier_count', 'inertia_per_member'],
});
const NAMES = Object.keys(EXPECTED);
const SHA_PATTERN = /^[0-9a-f]{64}$/;

function need(ok, message) {
  if (!ok) throw new Error('Gate 9.2 profile invalid: ' + message);
}
function close(a, b, absolute = 1e-9) {
  return Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= absolute + 1e-9 * Math.max(Math.abs(a), Math.abs(b));
}
function isObject(x) { return x !== null && typeof x === 'object' && !Array.isArray(x); }
function sameArray(a, b) { return Array.isArray(a) && a.length === b.length && a.every((v,i) => v === b[i]); }
function sameKeys(o, keys) { return isObject(o) && Object.keys(o).length === keys.length && keys.every(k => Object.hasOwn(o,k)); }
function sha(raw) { return createHash('sha256').update(raw).digest('hex'); }
function verifyFile(raw, expected, name) {
  need(typeof expected === 'string' && SHA_PATTERN.test(expected), name + ' SHA format');
  // Gate 9.2 exports LF CSV. Windows Git checkout may convert text files to CRLF.
  const canonicalLF = raw.toString('utf8').replace(/\r\n/g, '\n');
  need(sha(raw) === expected || sha(Buffer.from(canonicalLF,'utf8')) === expected,
    name + ' checksum mismatch');
}
function csvRows(raw, header, name) {
  const txt = raw.toString('utf8').replace(/\r\n/g, '\n');
  need(!txt.includes('\r') && txt.endsWith('\n'), name + ' line endings or terminator');
  const lines = txt.slice(0,-1).split('\n');
  need(lines.length >= 2 && lines[0] === header.join(','), name + ' header mismatch');
  return lines.slice(1).map((line, i) => {
    need(line.length > 0 && !line.includes('"'), name + ' unsupported/empty CSV record ' + i);
    const fields = line.split(',');
    need(fields.length === header.length, name + ' column count mismatch');
    return Object.fromEntries(header.map((key,j)=>[key,fields[j]]));
  });
}
function decimal(raw, label, { integer=false, positive=false, nonnegative=false }={}) {
  need(typeof raw === 'string' && /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/.test(raw),label+' must be numeric');
  const v = Number(raw);
  need(Number.isFinite(v) && (!integer || Number.isSafeInteger(v)) &&
    (!positive || v>0) && (!nonnegative || v>=0), label+' out of range');
  return v;
}
function objectData(row) {
  return Object.fromEntries(FEATURES.map(f=>[f,decimal(row[f],f,{nonnegative:true})]));
}
function clusters(rows,name) {
  need(rows.length===2, name+' must contain exactly 2 clusters');
  const map = new Map();
  for(const r of rows) {
    const id=decimal(r.cluster,name+'.cluster',{integer:true,nonnegative:true});
    need(id<2 && !map.has(id),name+' duplicate/invalid cluster ID');
    map.set(id,r);
  }
  need(map.has(0)&&map.has(1),name+' incomplete');
  return [map.get(0),map.get(1)];
}
function category(rows, name, field, codes, sizes) {
  need(rows.length===2*codes.length,name+' row count');
  const seen = new Set();
  const counts = [0,0],shares = [0,0];
  const output = rows.map(r => {
    const cluster_id = decimal(r.cluster, name+'.cluster',{integer:true,nonnegative:true});
    const category = decimal(r[field], name+'.'+field,{integer:true,positive:true});
    const count=decimal(r.count,name+'.count',{integer:true,nonnegative:true});
    const within_cluster_share=decimal(r.within_cluster_share,name+'.within_cluster_share',{nonnegative:true});
    const key = cluster_id+':'+category;
    need(cluster_id < 2 && codes.includes(category) && !seen.has(key),name+' unexpected/duplicate category');
    seen.add(key);
    need(count<=sizes[cluster_id].count && within_cluster_share<=1+1e-9,name+' category bound');
    need(close(within_cluster_share,count/sizes[cluster_id].count),name+' category share mismatch');
    counts[cluster_id]+=count; shares[cluster_id]+=within_cluster_share;
    return {cluster_id,[field.toLowerCase()]:category,count,within_cluster_share};
  });
  need(counts.every((n,i)=>n===sizes[i].count), name+' category totals mismatch');
  need(shares.every(n=>close(n,1)),name+' category shares do not sum to 1');
  return output.sort((a,b)=>a.cluster_id-b.cluster_id||a[field.toLowerCase()]-b[field.toLowerCase()]);
}

export function loadVerifiedFinalProfile(loaded, { profileDir = DEFAULT_DIR } = {}) {
  need(isObject(loaded) && isObject(loaded.model) && isObject(loaded.evaluation), 'frozen model unavailable');
  const m=loaded.model;
  const e=loaded.evaluation;
  const metadata=JSON.parse(readFileSync(join(profileDir,'profile_metadata.json'),'utf8'));
  const src=metadata.provenance;
  need(metadata.schema_version===1 && metadata.status==='COMPLETE' &&
    metadata.decision===m.selection_decision && metadata.decision==='D011' &&
    metadata.scope==='train_plus_validation' &&
    metadata.frozen_k===m.k && m.k===2 &&
    metadata.frozen_preprocessing===m.preprocessing &&
    metadata.development_count===m.training_count && m.training_count===352 &&
    sameArray(metadata.feature_columns,FEATURES) &&
    sameArray(metadata.profiling_only_columns,['Channel','Region']) &&
    metadata.model_fit_performed===false && metadata.scaler_fit_performed===false &&
    metadata.test_used===false &&
    metadata.source_rows?.train===264 && metadata.source_rows?.validation===88 &&
    metadata.source_policy==='read train.csv and validation.csv only; no final test or re-fit' &&
    metadata.distance_space==='Euclidean in frozen log1p StandardScaler space' &&
    metadata.outlier_policy==='distance > cluster Q3 + 1.5*IQR; descriptive flag, no removal' &&
    metadata.median_ratio_denominator==='overall 352-development median by feature' &&
    src?.model_sha256===loaded.checksum &&
    src?.selection_sha256===e.selection_sha256 &&
    typeof src?.train_sha256==='string' && SHA_PATTERN.test(src.train_sha256) &&
    typeof src?.validation_sha256==='string' && SHA_PATTERN.test(src.validation_sha256) &&
    sameKeys(metadata.files,NAMES) && sameKeys(metadata.cluster_counts,['0','1']),
    'metadata or Gate 5 provenance mismatch');

  const data={};
  for (const name of NAMES) {
    const record=metadata.files[name];
    need(record?.path==='reports/data/final_profile/'+name,'noncanonical file path '+name);
    const file=readFileSync(join(profileDir,name));
    verifyFile(file,record.sha256,name);
    data[name]=csvRows(file,EXPECTED[name],name);
  }
  const sourceProfiles=m.cluster_profiles;
  const summary=clusters(data['cluster_summary.csv'],'cluster_summary').map((row,i)=>{
    const count=decimal(row.count,'summary.count',{integer:true,positive:true});
    const share=decimal(row.share,'summary.share',{nonnegative:true});
    const median_spending=objectData(row);
    const p=sourceProfiles[i];
    need(row.profile_name===p.profile_name && count===p.count &&
      close(share,p.share) && close(share,count/352) &&
      FEATURES.every(f=>close(median_spending[f],p.median_spending[f])),
      'cluster summary disagrees with frozen model');
    need(metadata.cluster_counts[String(i)]===count,'metadata cluster counts');
    return {cluster_id:i,name:row.profile_name,count,share,median_spending};
  });
  need(summary[0].count+summary[1].count===352 && close(summary[0].share+summary[1].share,1),'development totals');

  const sizes=clusters(data['cluster_sizes.csv'],'cluster_sizes').map((row,i)=>{
    const count=decimal(row.count,'sizes.count',{integer:true,positive:true});
    const share=decimal(row.share,'sizes.share',{nonnegative:true});
    need(count===summary[i].count && close(share,summary[i].share),'cluster sizes mismatch');
    return {cluster_id:i,count,share};
  });
  const ratio=clusters(data['median_ratio.csv'],'median_ratio').map((row,i)=>({
    cluster_id:i,values:Object.fromEntries(FEATURES.map(f=>[f,decimal(row[f], 'median_ratio.'+f,{positive:true})])),
  }));
  // Every ratio is relative to the same overall-development median per feature.
  for(const f of FEATURES) {
    need(close(summary[0].median_spending[f]/ratio[0].values[f],
      summary[1].median_spending[f]/ratio[1].values[f],1e-7),
      'median ratio denominator mismatch '+f);
  }
  const channel=category(data['channel_profile.csv'],'channel_profile','Channel',[1,2],sizes);
  const region=category(data['region_profile.csv'],'region_profile','Region',[1,2,3],sizes);
  const dist=clusters(data['distance_summary.csv'],'distance_summary').map((row,i)=>{
    const count=decimal(row.count,'distance.count',{integer:true,positive:true});
    need(count===sizes[i].count,'distance cluster count');
    const keys=['min','mean','median','p90','p95','max','q1','q3','iqr_upper_fence','inertia_per_member'];
    const values=Object.fromEntries(keys.map(f=>[f,decimal(row[f],'distance.'+f,{nonnegative:true})]));
    const outlier_count=decimal(row.iqr_distance_outlier_count,'distance.outliers',{integer:true,nonnegative:true});
    need(values.min<=values.q1 && values.q1<=values.median &&
      values.median<=values.q3 && values.q3<=values.p90 && values.p90<=values.p95 &&
      values.p95<=values.max && values.min<=values.mean && values.mean<=values.max &&
      close(values.iqr_upper_fence, values.q3+1.5*(values.q3-values.q1)) &&
      outlier_count<=count && values.inertia_per_member>=values.mean*values.mean-1e-7,
      'distance distribution impossible');
    return {cluster_id:i,count,...values,iqr_distance_outlier_count:outlier_count};
  });
  const allOutliers=dist.reduce((n,r)=>n+r.iqr_distance_outlier_count,0);
  need(metadata.distance_outlier_count===allOutliers,'distance outlier total');
  const totalInertia=dist.reduce((n,r)=>n+r.count*r.inertia_per_member,0)/352;
  need(close(totalInertia,metadata.inertia_per_row) &&
    close(totalInertia,e.training.inertia_per_row),
    'frozen development inertia mismatch');
  need(metadata.top_1pct_count===4 &&
    typeof metadata.top_1pct_inertia_share==='number' &&
    Number.isFinite(metadata.top_1pct_inertia_share) &&
    metadata.top_1pct_inertia_share>=0 && metadata.top_1pct_inertia_share<=1,
    'invalid outlier concentration metadata');
  return {
    source_scope:'train_plus_validation',
    development_count:352,
    model_sha256:loaded.checksum,
    selection_sha256:e.selection_sha256,
    feature_columns:[...FEATURES],
    profiling_only_columns:['Channel','Region'],
    cluster_summary:summary,
    cluster_sizes:sizes,
    median_ratio:ratio,
    channel_profile:channel,
    region_profile:region,
    distance_summary:dist,
    outliers:{
      rule:metadata.outlier_policy,
      count:allOutliers,
      top_1pct_count:metadata.top_1pct_count,
      top_1pct_inertia_share:metadata.top_1pct_inertia_share,
    },
    inertia_per_row:metadata.inertia_per_row,
    distance_space:metadata.distance_space,
    median_ratio_denominator:metadata.median_ratio_denominator,
    evidence_sha256:Object.fromEntries(NAMES.map(name=>[name,metadata.files[name].sha256])),
    read_only:true,
    test_used:false,
  };
}
