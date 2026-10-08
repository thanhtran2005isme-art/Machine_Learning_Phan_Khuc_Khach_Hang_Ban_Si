import { test } from 'node:test';
import { strict as assert } from 'node:assert';
import { createHash } from 'node:crypto';
import { copyFileSync, mkdtempSync, readFileSync, rmSync, unlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadModel } from './model.mjs';
import { loadVerifiedFinalProfile } from './final-profile.mjs';

const source = fileURLToPath(new URL('../reports/data/final_profile/', import.meta.url));
const filenames = ['profile_metadata.json','cluster_summary.csv','median_ratio.csv',
  'cluster_sizes.csv','channel_profile.csv','region_profile.csv','distance_summary.csv'];
const loaded = loadModel();
const hash = x => createHash('sha256').update(x).digest('hex');

function fixture(callback) {
  const dir = mkdtempSync(join(tmpdir(),'gate9-3-profile-'));
  try {
    for(const filename of filenames) copyFileSync(join(source,filename),join(dir,filename));
    return callback(dir);
  } finally {
    rmSync(dir,{recursive:true,force:true});
  }
}
function modifyCsv(dir,name,rewrite) {
  const path=join(dir,name);
  const old=readFileSync(path,'utf8');
  writeFileSync(path,rewrite(old),'utf8');
}
function updateHash(dir,name) {
  const path=join(dir,'profile_metadata.json');
  const metadata=JSON.parse(readFileSync(path,'utf8'));
  metadata.files[name].sha256=hash(readFileSync(join(dir,name)));
  writeFileSync(path,JSON.stringify(metadata,null,2)+'\n');
}

test('Gate 9.3: dashboard profiles exactly match frozen K2 and 352 development', () => {
  const result=loadVerifiedFinalProfile(loaded);
  assert.equal(result.development_count,352);
  assert.deepEqual(result.cluster_sizes.map(x=>x.count),[162,190]);
  assert.deepEqual(result.cluster_summary.map(x=>x.name),loaded.model.cluster_profiles.map(x=>x.profile_name));
  assert.equal(result.channel_profile.reduce((sum,r)=>sum+r.count,0),352);
  assert.equal(result.region_profile.reduce((sum,r)=>sum+r.count,0),352);
  assert.equal(result.distance_summary.reduce((sum,r)=>sum+r.iqr_distance_outlier_count,0),16);
  assert.ok(Math.abs(result.inertia_per_row-loaded.evaluation.training.inertia_per_row)<1e-10);
  assert.equal(result.outliers.count,16);
  assert.equal(result.evidence_sha256['cluster_summary.csv'].length,64);
  assert.deepEqual(result.profiling_only_columns,['Channel','Region']);
  assert.equal(result.test_used,false);
  assert.equal(result.read_only,true);
});
test('Gate 9.3: every source CSV is checked against SHA-256, fail closed', () =>
  fixture(dir => {
    for(const name of filenames.filter(f=>f.endsWith('.csv'))) {
      modifyCsv(dir,name,s=>s+'\n');
      assert.throws(()=>loadVerifiedFinalProfile(loaded,{profileDir:dir}),
        /checksum mismatch/,'must reject '+name);
      copyFileSync(join(source,name),join(dir,name));
    }
  })
);
test('Gate 9.3: missing source CSV rejects instead of partial profile', () =>
  fixture(dir=>{
    unlinkSync(join(dir,'region_profile.csv'));
    assert.throws(()=>loadVerifiedFinalProfile(loaded,{profileDir:dir}),/ENOENT/);
  })
);
test('Gate 9.3: modified metadata model SHA/provenance is rejected', () =>
  fixture(dir=>{
    const path=join(dir,'profile_metadata.json');
    const metadata=JSON.parse(readFileSync(path,'utf8'));
    metadata.provenance.model_sha256='0'.repeat(64);
    writeFileSync(path,JSON.stringify(metadata),'utf8');
    assert.throws(()=>loadVerifiedFinalProfile(loaded,{profileDir:dir}),/provenance mismatch/);
  })
);
test('Gate 9.3: noncanonical metadata path rejects traversal', () =>
  fixture(dir=>{
    const path=join(dir,'profile_metadata.json');
    const meta=JSON.parse(readFileSync(path,'utf8'));
    meta.files['region_profile.csv'].path='../../models/model.json';
    writeFileSync(path,JSON.stringify(meta),'utf8');
    assert.throws(()=>loadVerifiedFinalProfile(loaded,{profileDir:dir}),/noncanonical file path/);
  })
);
test('Gate 9.3: semantic tampering still fails if CSV SHA is recalculated', () =>
  fixture(dir=>{
    modifyCsv(dir,'cluster_sizes.csv',s=>s.replace('0,162,','0,161,'));
    updateHash(dir,'cluster_sizes.csv');
    assert.throws(()=>loadVerifiedFinalProfile(loaded,{profileDir:dir}),/cluster sizes mismatch/);
  })
);
test('Gate 9.3: category count tampering with new valid SHA still fails', () =>
  fixture(dir=>{
    modifyCsv(dir,'channel_profile.csv',s=>s.replace('0,1,54,','0,1,53,'));
    updateHash(dir,'channel_profile.csv');
    assert.throws(()=>loadVerifiedFinalProfile(loaded,{profileDir:dir}),/category share mismatch|category totals mismatch/);
  })
);
test('Gate 9.3: invalid CSV shape with updated SHA rejects before parse', () =>
  fixture(dir=>{
    modifyCsv(dir,'median_ratio.csv',s=>s.replace('cluster,Fresh,','cluster,WRONG,'));
    updateHash(dir,'median_ratio.csv');
    assert.throws(()=>loadVerifiedFinalProfile(loaded,{profileDir:dir}),/header mismatch/);
  })
);
test('Gate 9.3: LF-to-CRLF checkout conversion on Windows is accepted', () =>
  fixture(dir=>{
    for(const name of filenames.filter(f=>f.endsWith('.csv'))) {
      modifyCsv(dir,name,s=>s.replace(/\r?\n/g,'\r\n'));
    }
    assert.equal(loadVerifiedFinalProfile(loaded,{profileDir:dir}).cluster_summary.length,2);
  })
);
test('Gate 9.3: read-only serving has no raw/train/validation/test dependency', () => {
  const before=filenames.map(name=>hash(readFileSync(join(source,name))));
  const result=loadVerifiedFinalProfile(loaded);
  assert.equal(result.source_scope,'train_plus_validation');
  const after=filenames.map(name=>hash(readFileSync(join(source,name))));
  assert.deepEqual(before,after);
});
