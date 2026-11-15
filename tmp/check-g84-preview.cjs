const {chromium}=require('/Users/wanghu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  const page=await browser.newPage({viewport:{width:780,height:650}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('file:///Users/wanghu/Documents/ChatGPT/加工工序学习/tmp/g84-preview.html');
  const frame=page.frameLocator('iframe');
  for (const expected of ['Z 0.00 mm','Z 6.00 mm']){
    await frame.getByRole('button',{name:'下一步',exact:true}).click();
    const got=await frame.locator('[data-readout]').textContent();
    if(got!==expected)throw Error('Readout '+got+' expected '+expected);
  }
  await page.screenshot({path:'/tmp/g84-wide.png'});
  await page.setViewportSize({width:360,height:700});
  await page.screenshot({path:'/tmp/g84-narrow.png'});
  const size=await frame.locator('#g84-face-rigid-tapping').evaluate(el=>({cw:el.clientWidth,sw:el.scrollWidth}));
  if(size.sw>size.cw+1)throw Error('Overflow '+JSON.stringify(size));
  await frame.getByRole('button',{name:'下一步',exact:true}).click();
  const dwell=await frame.locator('[data-detail]').textContent();
  if(!dwell.includes('0.01'))throw Error('P units missing');
  await frame.getByRole('button',{name:'下一步',exact:true}).click();
  if((await frame.locator('[data-readout]').textContent())!=='Z −1.00 mm')throw Error('Return failed');
  await frame.getByRole('button',{name:/播放过程|重播过程/}).click();
  await page.waitForTimeout(450);
  await frame.getByRole('button',{name:'暂停',exact:true}).click();
  if(errors.length)throw Error(errors.join('\n'));
  console.log('PASS: step coordinates, P units, synchronized replay, no horizontal overflow, no script errors');
  await browser.close();
})();
