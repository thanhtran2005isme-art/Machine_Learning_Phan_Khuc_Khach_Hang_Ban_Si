import { useState } from 'react';

type F = 'Fresh'|'Milk'|'Grocery'|'Frozen'|'Detergents_Paper'|'Delicassen';
const fields: {key:F;label:string}[] = [
  {key:'Fresh',label:'Hàng tươi'},{key:'Milk',label:'Sữa'},{key:'Grocery',label:'Tạp hóa'},
  {key:'Frozen',label:'Đông lạnh'},{key:'Detergents_Paper',label:'Chất tẩy rửa/giấy'},
  {key:'Delicassen',label:'Thực phẩm chế biến'},
];
const fmt=(v:number,digits=2)=>new Intl.NumberFormat('vi-VN',{maximumFractionDigits:digits}).format(v);
function csvCell(value:string|number){
  if(typeof value==='number')return Number.isFinite(value)?String(value):'';
  const safe=/^[=+\-@\t\r]/.test(value)?"'"+value:value;
  return '"'+safe.replace(/"/g,'""')+'"';
}
function exportCsv(name:string,rows:(string|number)[][]){
  const content='\ufeff'+rows.map(row=>row.map(csvCell).join(',')).join('\r\n')+'\r\n';
  const url=URL.createObjectURL(new Blob([content],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}
type Result={cluster_id:number;distance_to_centroid:number;distances_to_centroids:number[];
  warnings:string[];profile:{name:string;median_spending:Record<F,number>}};
export function CustomerInsight({input,result}:{input:Record<F,string>;result:Result}){
  const other=result.distances_to_centroids.find((_,i)=>i!==result.cluster_id);
  const data=fields.map(f=>({key:f.key,label:f.label,v:Number(input[f.key]),
    median:result.profile.median_spending[f.key]}));
  function download(){exportCsv('kaitokidshop-ket-qua-phan-khuc.csv',[
    ['Decision','D011 frozen KMeans K2'],['Unit','annual monetary units (m.u.)'],
    ['Cluster',result.cluster_id],['Profile',result.profile.name],
    ['Distance to assigned centroid',result.distance_to_centroid],
    ['Distance to other centroid',other??''],['Warnings',result.warnings.join('; ')],
    ['Feature','Input','Cluster median','Input / median'],
    ...data.map(r=>[r.key,r.v,r.median,r.median>0?r.v/r.median:'N/A']),
  ])}
  return <section className="analysis-extra" aria-label="Giải thích kết quả từng khách">
    <h3>Giải thích kết quả từng khách</h3>
    <p className="muted small-note">Đầu vào so với median cụm được gán; cùng đơn vị m.u. theo năm.</p>
    <div className="customer-mini-chart" aria-label="So sánh từng khoản chi tiêu với median cụm">
      {data.map(row => {
        const denominator=Math.max(1,row.v,row.median);
        return <div className="customer-mini-row" key={row.key}>
          <span>{row.label}</span>
          <div className="customer-mini-bars">
            <div className="customer-mini-track"><span className="mini-input" style={{width:(row.v/denominator*100)+'%'}} /></div>
            <div className="customer-mini-track"><span className="mini-median" style={{width:(row.median/denominator*100)+'%'}} /></div>
          </div>
          <strong>{row.median>0?fmt(row.v/row.median)+'×':'—'}</strong>
        </div>;
      })}
      <p className="muted small-note">Mỗi hàng có thang riêng · <span className="legend-swatch input-swatch"/> Đầu vào · <span className="legend-swatch median-swatch"/> Median cụm</p>
    </div>
    <div className="table-scroll"><table className="data-table">
      <thead><tr><th>Nhóm hàng</th><th>Đầu vào</th><th>Median cụm</th><th>Tỷ lệ</th></tr></thead>
      <tbody>{data.map(r=><tr key={r.key}><th scope="row">{r.label}</th><td>{fmt(r.v)}</td>
        <td>{fmt(r.median)}</td><td>{r.median>0?fmt(r.v/r.median)+'×':'N/A'}</td></tr>)}</tbody>
    </table></div>
    <dl className="analysis-distances"><div><dt>Tâm được gán</dt><dd>{fmt(result.distance_to_centroid,4)}</dd></div>
      <div><dt>Tâm còn lại</dt><dd>{other===undefined?'—':fmt(other,4)}</dd></div>
      <div><dt>Chênh lệch khoảng cách</dt><dd>{other===undefined?'—':fmt(other-result.distance_to_centroid,4)}</dd></div></dl>
    <p className="muted small-note">Gán cụm dựa trên tâm gần nhất ở không gian log1p + StandardScaler 6 chiều. Chênh lệch khoảng cách không phải độ tin cậy, xác suất hay thang xếp hạng khách hàng.</p>
    <div className="analysis-actions"><button type="button" className="btn-subtle" onClick={download}>Tải CSV kết quả</button>
      <button type="button" className="btn-subtle" onClick={()=>window.print()}>In / lưu PDF</button></div>
  </section>;
}
type Experiment={preprocessing:string;k:number;train_inertia:number;validation_silhouette:number;
  validation_silhouette_std:number;ari:number;ari_min:number;ari_max:number;pair_count:number;
  min_cluster_share:number};
type Profile={development_count:number;outliers:{count:number;top_1pct_count:number;top_1pct_inertia_share:number}};
export function ExperimentReport({experiments,profile}:{experiments:Experiment[];profile:Profile}){
  const rows=[...experiments].sort((a,b)=>a.k-b.k||a.preprocessing.localeCompare(b.preprocessing));
  if(rows.length!==14||rows.some(x=>x.pair_count!==45||!Number.isFinite(x.ari_min)||!Number.isFinite(x.validation_silhouette_std)))
    return <p className="notice notice-error" role="alert">Thiếu bằng chứng độ nhạy seed; không hiển thị số liệu thay thế.</p>;
  function download(){exportCsv('kaitokidshop-thi-nghiem.csv',[
    ['Scope','train/validation only; no final test selection'],
    ['Mode','K','Train inertia','Validation silhouette','Silhouette SD','ARI mean','ARI min','ARI max','ARI pairs','Smallest cluster share'],
    ...rows.map(x=>[x.preprocessing,x.k,x.train_inertia,x.validation_silhouette,x.validation_silhouette_std,
      x.ari,x.ari_min,x.ari_max,x.pair_count,x.min_cluster_share]),
  ])}
  return <section className="analysis-extra" aria-label="Bảng bằng chứng thí nghiệm chuyên sâu">
    <h3>Bảng thí nghiệm chuyên sâu</h3>
    <p className="muted small-note">14 candidate · 10 seed/candidate · 45 cặp ARI/candidate. Dữ liệu đọc từ evidence đã lưu, không train lại.</p>
    <div className="table-scroll"><table className="data-table" aria-label="Bảng so sánh seed và K">
      <thead><tr><th>Biểu diễn</th><th>K</th><th>Silhouette val.</th><th>SD val.</th><th>ARI mean</th><th>ARI min</th><th>Cụm nhỏ nhất</th></tr></thead>
      <tbody>{rows.map(x=><tr key={x.preprocessing+x.k}><th scope="row">{x.preprocessing==='raw'?'Raw':'Log + Scale'}</th>
        <td>{x.k}</td><td>{fmt(x.validation_silhouette,4)}</td><td>{fmt(x.validation_silhouette_std,5)}</td>
        <td>{fmt(x.ari,4)}</td><td>{fmt(x.ari_min,4)}</td><td>{fmt(x.min_cluster_share*100,2)}%</td></tr>)}</tbody>
    </table></div>
    <p className="muted small-note">ARI so sánh phân hoạch, không đo tỷ lệ mã cụm giữ nguyên. SD ở đây phản ánh thay đổi seed trên validation cố định.</p>
    <div className="analysis-outlier"><h3>Ảnh hưởng của điểm xa (mô tả)</h3>
      <p>{profile.outliers.count}/{profile.development_count} khách vượt ngưỡng Q3 + 1,5×IQR của khoảng cách tới tâm theo cụm ({fmt(profile.outliers.count/profile.development_count*100,2)}%). {profile.outliers.top_1pct_count} điểm xa nhất đóng góp {fmt(profile.outliers.top_1pct_inertia_share*100,2)}% tổng squared distance.</p>
      <p className="muted small-note">Đây không phải thí nghiệm loại outlier; không thay đổi dữ liệu hoặc centroid đã đóng băng.</p>
    </div>
    <div className="analysis-actions"><button type="button" className="btn-subtle" onClick={download}>Tải CSV thí nghiệm</button>
      <button type="button" className="btn-subtle" onClick={()=>window.print()}>In / lưu PDF</button></div>
  </section>;
}
const points=[['An',1,1],['Bình',2,1],['Chi',3,3],['Dung',5,4],['Hà',6,5],['Lan',7,5]] as const;
const states=[
 {centers:[[1,1],[3,3]],labels:[0,0,1,1,1,1],heading:'1 · Khởi tạo và gán cụm',note:'Đặt tâm tại An và Chi, gán từng điểm cho tâm gần nhất.'},
 {centers:[[1.5,1],[5.25,4.25]],labels:[0,0,1,1,1,1],heading:'2 · Cập nhật tâm',note:'Tâm mới là trung bình tọa độ của từng cụm: (1,5;1) và (5,25;4,25).'},
 {centers:[[2,5/3],[6,14/3]],labels:[0,0,0,1,1,1],heading:'3 · Gán lại, hội tụ',note:'Chi chuyển sang cụm 0. Cập nhật tâm cho J=22/3 ≈ 7,3333.'},
];
export function LloydWalkthrough(){
  const [step,setStep]=useState(0);const state=states[step];const px=(x:number)=>24+(x-.5)*45;
  const py=(y:number)=>265-(y-.5)*41;
  return <section className="content-card" aria-label="Minh họa Lloyd với điểm mô phỏng">
    <div className="section-heading"><h2>K-Means hoạt động như thế nào?</h2>
      <p>Sáu điểm mô phỏng từ Bài 8 của giảng viên; không phải 440 khách Wholesale hay model phục vụ.</p></div>
    <div className="toy-layout">
      <svg className="toy-svg" viewBox="0 0 355 280" role="img"
        aria-label={points.map((p,i)=>p[0]+' cụm '+state.labels[i]).join(', ')}>
        {points.map((p,i)=><g key={p[0]}><circle cx={px(p[1])} cy={py(p[2])} r="8"
          fill={state.labels[i]===0?'#16826b':'#d5953a'} stroke="#fff" strokeWidth="2"/>
          <text x={px(p[1])+11} y={py(p[2])-9} fill="currentColor" fontSize="12">{p[0]}</text></g>)}
        {state.centers.map((p,i)=><path key={i} stroke={i===0?'#085941':'#986022'} strokeWidth="3"
          d={'M '+(px(p[0])-7)+' '+(py(p[1])-7)+' l 14 14 m 0 -14 l -14 14'}/>)}
      </svg>
      <div aria-live="polite"><h3>{state.heading}</h3><p>{state.note}</p>
        <p className="muted small-note">Chấm là khách mô phỏng, dấu × là centroid; mã 0/1 không có thứ bậc.</p>
        <div className="analysis-actions">
          <button type="button" className="btn-subtle" disabled={step===0} onClick={()=>setStep(s=>Math.max(0,s-1))}>Bước trước</button>
          <button type="button" className="btn-subtle" disabled={step===2} onClick={()=>setStep(s=>Math.min(2,s+1))}>Bước tiếp</button>
        </div>
        <p className="muted small-note">J là tổng bình phương khoảng cách tới tâm. J giảm không tự chứng minh K tốt hơn hoặc giá trị kinh doanh.</p>
      </div>
    </div>
  </section>;
}
