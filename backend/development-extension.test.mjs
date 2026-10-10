import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, cpSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { loadModel } from './model.mjs';
import { loadVerifiedDevelopmentExtension } from './development-extension.mjs';

const dir=fileURLToPath(new URL('../reports/data/development_extension/',import.meta.url));
const loaded=loadModel();
test('Gate10.2: frozen 352-development PCA/Ward evidence verified without training',()=>{
  const data=loadVerifiedDevelopmentExtension(loaded);
  assert.equal(data.points.length,352);
  assert.equal(data.points.filter(x=>x.split==='train').length,264);
  assert.equal(data.points.filter(x=>x.split==='validation').length,88);
  assert.deepEqual(data.comparison.frozen_counts,[162,190]);
  assert.equal(data.read_only,true);
  assert.equal(data.test_used,false);
  assert.ok(data.pca.explained_variance_ratio.reduce((a,b)=>a+b,0)>0.7);
});
test('Gate10.2: tampered points are rejected even when parseable',()=>{
  const tmp=mkdtempSync(join(tmpdir(),'gate10-extension-'));
  try{
    cpSync(dir,tmp,{recursive:true});
    const path=join(tmp,'analysis.json');
    const parsed=JSON.parse(readFileSync(path,'utf8'));
    parsed.points[0].pc1+=1;
    writeFileSync(path,JSON.stringify(parsed));
    assert.throws(()=>loadVerifiedDevelopmentExtension(loaded,{extensionDir:tmp}),/SHA256 mismatch/);
  } finally {rmSync(tmp,{recursive:true,force:true})}
});
test('Gate10.2: inconsistent metadata fails closed',()=>{
  const tmp=mkdtempSync(join(tmpdir(),'gate10-extension-'));
  try{
    cpSync(dir,tmp,{recursive:true});
    const path=join(tmp,'metadata.json');
    const parsed=JSON.parse(readFileSync(path,'utf8'));
    parsed.test_used=true;
    writeFileSync(path,JSON.stringify(parsed));
    assert.throws(()=>loadVerifiedDevelopmentExtension(loaded,{extensionDir:tmp}),/metadata\/provenance/);
  } finally {rmSync(tmp,{recursive:true,force:true})}
});
