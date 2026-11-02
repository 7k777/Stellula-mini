// Stellula Mini PWA：前端仅使用基础 JavaScript，不含正式项目的私有前端代码。
// 为避免在公开演示中泄露或误操作正式后端，默认只读取本仓库的演示数据。
const $ = (id) => document.getElementById(id);
let competitions = [];
function escapeHtml(value) {
  // 防止数据被当作 HTML 注入页面。
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
function match(item, major, year, interest) {
  if (year && item.years.length && !item.years.includes(Number(year))) return null;
  let score = 0;
  const reasons = [];
  if (major) {
    if (item.majors.includes(major)) {score += 70; reasons.push("专业直接匹配");}
    else if (item.majors.includes("不限专业")) {score += 25; reasons.push("跨专业拓展选择");}
  }
  if (interest && item.interests.some(x => x.toLowerCase().includes(interest.toLowerCase()))) {
    score += 30; reasons.push("兴趣方向相关");
  }
  if ((major || interest) && score === 0) return null;
  return {...item, score, reasons};
}
function render() {
  const major=$("major").value.trim(), year=$("year").value.trim(), interest=$("interest").value.trim();
  if (year && (+year<1 || +year>8 || !Number.isInteger(+year))) {$("status").textContent="年级请输入 1～8 的整数";$("results").innerHTML="";return;}
  const found=competitions.map(x=>match(x,major,year,interest)).filter(Boolean).sort((a,b)=>b.score-a.score||a.id-b.id);
  $("status").textContent="演示模式 · 所有竞赛均为虚构样例"; $("count").textContent="· "+found.length+" 项";
  $("results").innerHTML=found.length ? found.map(c=>`<article class="result"><div class="score">${c.score} 分</div><div class="result-title">${escapeHtml(c.name)}</div><div class="muted">${escapeHtml(c.summary)}</div><div class="muted">适用专业：${escapeHtml(c.majors.join("、"))}</div>${c.reasons.map(r=>`<span class="pill">${escapeHtml(r)}</span>`).join("")}</article>`).join("") : '<div id="empty">暂时没有匹配的赛事，可以换个条件试试。</div>';
}
async function start() {
 try {const response=await fetch("./demo-data.json");if(!response.ok)throw Error("load");competitions=await response.json();render();}
 catch(e){$("status").textContent="演示数据加载失败，请联网后刷新。";}
}
$("search").addEventListener("click",render);
$("reset").addEventListener("click",()=>{$("major").value="";$("year").value="";$("interest").value="";render();});
if ("serviceWorker" in navigator && location.protocol==="https:") navigator.serviceWorker.register("./sw.js").catch(()=>{});
start();