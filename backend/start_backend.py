#!/usr/bin/env python3
"""
Script Python para iniciar o backend sem avisos do sandbox
"""
import os
import sys
import subprocess

# Suprimir avisos do sandbox
os.environ['ELECTRON_DISABLE_SANDBOX'] = '1'
os.environ['CHROME_DISABLE_SANDBOX'] = '1'
os.environ['NO_SANDBOX'] = '1'

# Redirecionar stderr para suprimir avisos
with open(os.devnull, 'w') as devnull:
    # Iniciar uvicorn
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'app.main:app',
            '--reload',
            '--port', '8000'
        ], stderr=devnull)
    except KeyboardInterrupt:
        print("\n✅ Backend encerrado")

