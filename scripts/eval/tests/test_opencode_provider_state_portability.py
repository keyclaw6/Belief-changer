from __future__ import annotations
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / ".opencode/plugins/provider-state-portability.js"


class ProviderStatePortabilityPluginTests(unittest.TestCase):
    def test_plugin_strips_only_stale_reasoning_provider_state(self):
        script = r'''
import ProviderStatePortability from PROCESS_PLUGIN;
process.env.OPENCODE_RDC_PROVIDER_STATE_SESSION_ID = "ses_test";
process.env.OPENCODE_RDC_PROVIDER_STATE_CUTOFF_MS = "200";
const hooks = await ProviderStatePortability();
const output = {messages:[{info:{id:"m"},parts:[
  {id:"old",type:"reasoning",sessionID:"ses_test",messageID:"m",text:"",time:{start:100},metadata:{openai:{itemId:"opaque-old",reasoningEncryptedContent:"cipher-old",keep:"x"},other:{keep:true}}},
  {id:"future",type:"reasoning",sessionID:"ses_test",messageID:"m",text:"",time:{start:300},metadata:{openai:{itemId:"opaque-new",reasoningEncryptedContent:"cipher-new"}}},
  {id:"other-session",type:"reasoning",sessionID:"ses_other",messageID:"m",text:"",time:{start:100},metadata:{openai:{itemId:"opaque-other",reasoningEncryptedContent:"cipher-other"}}},
  {id:"text",type:"text",sessionID:"ses_test",messageID:"m",text:"visible",time:{start:100},metadata:{openai:{itemId:"must-stay"}}},
] }]};
await hooks["experimental.chat.messages.transform"]({}, output);
console.log(JSON.stringify(output));
'''.replace("PROCESS_PLUGIN", json.dumps(PLUGIN.as_uri()))
        proc = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT,
                              capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        parts = {p["id"]: p for p in data["messages"][0]["parts"]}
        self.assertEqual(parts["old"]["metadata"]["openai"], {"keep": "x"})
        self.assertEqual(parts["old"]["metadata"]["other"], {"keep": True})
        self.assertEqual(parts["future"]["metadata"]["openai"]["itemId"], "opaque-new")
        self.assertEqual(parts["other-session"]["metadata"]["openai"]["itemId"], "opaque-other")
        self.assertEqual(parts["text"]["metadata"]["openai"]["itemId"], "must-stay")

    def test_plugin_is_noop_without_recovery_marker(self):
        script = r'''
import ProviderStatePortability from PROCESS_PLUGIN;
delete process.env.OPENCODE_RDC_PROVIDER_STATE_SESSION_ID;
delete process.env.OPENCODE_RDC_PROVIDER_STATE_CUTOFF_MS;
const hooks = await ProviderStatePortability();
const output = {messages:[{info:{id:"m"},parts:[
  {id:"old",type:"reasoning",sessionID:"ses_test",messageID:"m",text:"",time:{start:100},metadata:{openai:{itemId:"opaque",reasoningEncryptedContent:"cipher"}}}
]}]};
const before = JSON.stringify(output);
await hooks["experimental.chat.messages.transform"]({}, output);
console.log(JSON.stringify({same:before===JSON.stringify(output)}));
'''.replace("PROCESS_PLUGIN", json.dumps(PLUGIN.as_uri()))
        proc = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT,
                              capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(proc.stdout)["same"])


if __name__ == "__main__":
    unittest.main()
