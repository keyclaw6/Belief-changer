// Scoped state transfer on the owned research endpoint. Secrets stay on pipes.
const fs = require('node:fs');
const crypto = require('node:crypto');

function permitted(host, domains) {
  host = host.toLowerCase().replace(/^\./, '');
  return domains.some(d => host === d || host.endsWith('.' + d));
}

function filterState(state, domains) {
  const origins = (state.origins || []).filter(o => {
    try { const u = new URL(o.origin); return u.protocol === 'https:' && u.origin === o.origin && (!u.port || u.port==='443') && permitted(u.hostname, domains); }
    catch { return false; }
  });
  const result = {cookies:(state.cookies || []).filter(c => permitted(c.domain || '', domains)), origins};
  if (Array.isArray(state.credentials)) result.credentials = state.credentials.filter(c => permitted(c.rpId || '', domains));
  return result;
}

async function main() {
  const [operation, endpoint, modulePath, encodedDomains] = process.argv.slice(2);
  const domains = JSON.parse(encodedDomains);
  const {chromium} = require(modulePath);
  const browser = await chromium.connectOverCDP(endpoint);
  try {
    const context = browser.contexts()[0];
    if (!context) throw new Error('Missing owned context');
    if (operation === 'bridge-id') {
      const identities=[];
      for (const worker of context.serviceWorkers()) {
        if (!worker.url().startsWith('chrome-extension://')) continue;
        const identity=await worker.evaluate(async()=> {
          const m=chrome.runtime.getManifest();
          if (m.name!=='OpenCLI') return null;
          const id=(await chrome.storage.local.get('opencli_context_id_v1')).opencli_context_id_v1;
          return {contextId:id,version:m.version};
        });
        if (identity) identities.push(identity);
      }
      if (identities.length!==1 || !identities[0].contextId) throw new Error('Owned bridge identity unavailable');
      process.stdout.write(JSON.stringify(identities[0]));
    } else if (operation === 'export') {
      const state = filterState(await context.storageState({indexedDB:true,opfs:true,credentials:true}), domains);
      const sessions = {};
      for (const page of context.pages()) {
        let u; try {u = new URL(page.url());} catch {continue;}
        if (u.protocol !== 'https:' || !permitted(u.hostname, domains)) continue;
        // A CDP client did not observe navigation done by another controller;
        // explicitly include live origin storage instead of relying on its cache.
        const local = await page.evaluate(() => Array.from({length:localStorage.length},(_,i)=> {
          const name=localStorage.key(i);return {name,value:localStorage.getItem(name)};
        }));
        let origin = state.origins.find(o=>o.origin===u.origin);
        if (!origin) {origin={origin:u.origin,localStorage:[]};state.origins.push(origin);}
        origin.localStorage=local;
        const values = await page.evaluate(() => Object.fromEntries(Object.keys(sessionStorage).map(k=>[k,sessionStorage.getItem(k)])));
        if (Object.keys(values).length) sessions[u.origin] = values;
      }
      const restoreId = crypto.randomUUID();
      for (const origin of Object.keys(sessions)) {
        let o = state.origins.find(x=>x.origin===origin);
        if (!o) {o={origin,localStorage:[]};state.origins.push(o);}
        o.localStorage = (o.localStorage || []).filter(x=>x.name!=='__bc_session_restore');
        o.localStorage.push({name:'__bc_session_restore',value:restoreId});
      }
      process.stdout.write(JSON.stringify({version:1,state,sessions,restoreId}));
    } else if (operation === 'import' || operation === 'import-watch') {
      let raw=''; for await (const chunk of process.stdin) raw+=chunk;
      const bundle=JSON.parse(raw);raw='';
      if (bundle.version!==1) throw new Error('Unsupported state version');
      const state=filterState(bundle.state,domains);
      await context.setStorageState(state);
      const sessions=Object.fromEntries(Object.entries(bundle.sessions || {}).filter(([origin])=> {
        try {let u=new URL(origin);return u.protocol==='https:'&&permitted(u.hostname,domains);} catch{return false;}
      }));
      await context.addInitScript(({sessions,id})=> {
        if (localStorage.getItem('__bc_session_restore')!==id) return;
        for (const [k,v] of Object.entries(sessions[location.origin] || {})) if (sessionStorage.getItem(k)===null) sessionStorage.setItem(k,v);
        localStorage.removeItem('__bc_session_restore');
      }, {sessions,id:bundle.restoreId});
      process.stdout.write(JSON.stringify({imported:true})+'\n');
      if (operation==='import-watch') {
        // CDP init-script installation for future tabs belongs to this client.
        // Keep it attached for the lifetime of the owned browser, not one RPC.
        await new Promise(resolve=>process.once('SIGTERM',resolve));
      }
    } else throw new Error('Unsupported operation');
  } finally {await browser.close();}
}

if (require.main===module) main().catch(()=> {process.stderr.write('Private browser-state transfer failed.\n');process.exitCode=1;});
module.exports={permitted,filterState};
