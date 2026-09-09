import sys
import urllib.request
import json
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

# Start uvicorn on port 8008 in background
proc = subprocess.Popen(['python', '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8008'])
time.sleep(3)

try:
    # 1. Test Translate Single endpoint
    req = urllib.request.Request(
        'http://127.0.0.1:8008/api/translate',
        data=json.dumps({'text': 'capital subsidy', 'target_language': 'ta'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print('Translate Single (Tamil):', res)

    # 2. Test Translate Batch endpoint
    req_b = urllib.request.Request(
        'http://127.0.0.1:8008/api/translate/batch',
        data=json.dumps({
            'texts': [
                'Your annual family income falls comfortably within scheme eligibility guidelines.',
                'Your business location qualifies for special higher rural capital subsidy.'
            ],
            'target_language': 'hi'
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req_b) as resp_b:
        res_b = json.loads(resp_b.read().decode('utf-8'))
        print('Translate Batch (Hindi):', res_b)

    # 3. Test Lexicon endpoint
    with urllib.request.urlopen('http://127.0.0.1:8008/api/translate/lexicon') as resp_l:
        res_l = json.loads(resp_l.read().decode('utf-8'))
        print('Lexicon endpoint status: 200, corpus size:', res_l.get('explainability_corpus_size'))

finally:
    proc.terminate()
    proc.wait()
    print('Cleaned up backend test process.')
