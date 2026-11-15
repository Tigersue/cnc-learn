const fs = require('fs');
const vm = require('vm');
const {createRequire}=require('module');
const taskRequire=createRequire('/Users/wanghu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const sharp=taskRequire('sharp');
const html=fs.readFileSync('/Users/wanghu/.codex/visualizations/2026/10/30/01a18a58-57a3-79d2-b318-31201a129eaf/g94-facing-cycle.html','utf8');
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
let width=736;
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.attrs={};this.textContent='';this.handlers={};this.value=0;}
  setAttribute(k,v){this.attrs[k]=v;}
  appendChild(n){this.children.push(n);return n;}
  replaceChildren(){this.children=[];}
  getBoundingClientRect(){return {width};}
  addEventListener(k,f){this.handlers[k]=f;}
}
const ids={};
for(const match of html.matchAll(/id="([^"]+)"/g))ids[match[1]]=new Element('div');
ids['g94-facing-teach'].querySelector=s=>ids[s.slice(1)];
let resize;
let raf;
let saved;
const ctx={document:{getElementById:id=>ids[id],createElementNS:(_ns,tag)=>new Element(tag)},window:{openai:{setWidgetState:state=>{saved=state;return Promise.resolve();}},addEventListener(){}},ResizeObserver:class{constructor(f){resize=f;}observe(){}},requestAnimationFrame:f=>{raf=f;},matchMedia:()=>({matches:false}),Math,Number,String,Object};
vm.runInNewContext(code,ctx);
function assert(test,label){if(!test)throw Error(label);}
const txt=()=>ids['g94-detail'].textContent;
assert(txt().includes('X16.600 / Z−1.000'),'start');
const expected=[['16.600','4.000'],['8.000','4.000'],['8.000','−1.000'],['16.600','−1.000'],['16.600','8.000'],['8.000','8.000'],['8.000','−1.000'],['16.600','−1.000'],['16.600','12.000'],['8.000','12.000'],['8.000','−1.000'],['16.600','−1.000']];
for(const [x,z]of expected){ids['g94-next'].handlers.click();assert(txt().includes('X'+x+' / Z'+z),'step: '+txt());}
assert(ids['g94-next'].disabled,'final next disabled');
assert(txt().includes('三刀完成'),'finished');
ids['g94-prev'].handlers.click();assert(txt().includes('X8.000 / Z−1.000'),'previous');
ids['g94-seek'].value=150;ids['g94-seek'].handlers.input();assert(txt().includes('X12.300 / Z4.000'),'scrubbing');
ids['g94-seek'].handlers.change();assert(saved.privateContent.position===1.5,'save state');
ids['g94-play'].handlers.click();raf(1000);raf(1200);assert(txt().includes('X11.518'),'play updates');
ids['g94-play'].handlers.click();
function serialize(n){const escape=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');return '<'+n.tag+Object.entries(n.attrs).map(([k,v])=>' '+k+'="'+escape(v)+'"').join('')+'>'+escape(n.textContent)+n.children.map(serialize).join('')+'</'+n.tag+'>';}
const css=`text{fill:#182433;font:12px 'Hiragino Sans GB','PingFang SC',sans-serif}.g94-struct{stroke:#d0d7df;stroke-width:1;fill:none}.g94-axis{stroke:#697a8b;stroke-width:1}.g94-stock{fill:#e4eaf0;stroke:#687a8c;stroke-width:1}.g94-feed{stroke:#1e70ae;stroke-width:2;fill:none}.g94-rapid{stroke:#697a8b;stroke-width:1.5;stroke-dasharray:5 4;fill:none}.g94-active{stroke-width:4}.g94-tool{fill:#1e70ae;stroke:#fff;stroke-width:1.5}`;
(async()=>{
  for(const w of [320,736]){
    width=w;resize();
    let s=serialize(ids['g94-drawing'].children[0]).replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="346" ');
    s=s.replace(/(<svg[^>]*>)/,'$1<style>'+css+'</style>');
    await sharp(Buffer.from(s)).png().toFile('/tmp/g94-check-'+w+'.png');
  }
  console.log('PASS: 12 segment endpoints, next/previous, scrubbing, play/pause, saved state; SVG renders at 320 and 736 px.');
})().catch(e=>{console.error(e);process.exitCode=1;});
