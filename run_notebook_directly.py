"""
Direct in-process executor for EDA_Lesson_Notebook.ipynb
Executes all cells, captures printed output and results, and saves the notebook with outputs.
"""
import os
os.environ['MPLCONFIGDIR'] = r'c:\Users\Hp\Downloads\hcl\.mplconfig'
import io, json, sys, traceback
from contextlib import redirect_stdout, redirect_stderr
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Set plotly renderer to 'json' so it computes figures without trying to spawn external browsers
pio.renderers.default = "json"

nb_path = r'c:\Users\Hp\Downloads\hcl\EDA_Lesson_Notebook.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

global_scope = {
    '__name__': '__main__',
    '__file__': nb_path,
}

code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
print(f"Total code cells to execute: {len(code_cells)}")

exec_count = 1
for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    
    source = ''.join(cell['source'])
    first_line = source.strip().split('\n')[0] if source.strip() else 'empty'
    print(f"[{exec_count}/{len(code_cells)}] Running: {first_line[:55]}...", flush=True)
    
    cell['execution_count'] = exec_count
    cell['outputs'] = []
    
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    
    try:
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            try:
                # If the entire cell is an expression (e.g. df.head(), df.info()), eval it to capture the result
                compiled = compile(source.strip(), '<cell>', 'eval')
                res = eval(compiled, global_scope)
                if res is not None:
                    if isinstance(res, (pd.DataFrame, pd.Series)):
                        cell['outputs'].append({
                            'output_type': 'execute_result',
                            'execution_count': exec_count,
                            'data': {
                                'text/plain': repr(res),
                                'text/html': res._repr_html_() if hasattr(res, '_repr_html_') else repr(res)
                            },
                            'metadata': {}
                        })
                    else:
                        cell['outputs'].append({
                            'output_type': 'execute_result',
                            'execution_count': exec_count,
                            'data': {
                                'text/plain': repr(res)
                            },
                            'metadata': {}
                        })
            except SyntaxError:
                # Statements, loops, definitions, or multi-line assignments: execute standard
                exec(source, global_scope)
                
        out_text = stdout_buf.getvalue()
        if out_text:
            cell['outputs'].append({
                'output_type': 'stream',
                'name': 'stdout',
                'text': out_text.splitlines(keepends=True)
            })
            
        err_text = stderr_buf.getvalue()
        if err_text:
            cell['outputs'].append({
                'output_type': 'stream',
                'name': 'stderr',
                'text': err_text.splitlines(keepends=True)
            })
            
    except Exception as e:
        err_msg = traceback.format_exc()
        print(f"❌ Error in cell {exec_count}:\n{err_msg}", flush=True)
        cell['outputs'].append({
            'output_type': 'error',
            'ename': type(e).__name__,
            'evalue': str(e),
            'traceback': err_msg.splitlines(keepends=True)
        })
        sys.exit(1)
        
    exec_count += 1
    plt.close('all')

print(f"\n🎉 ALL {len(code_cells)} CODE CELLS EXECUTED WITH 100% SUCCESS!", flush=True)

# Save the executed notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Saved executed notebook to: {nb_path} ({os.path.getsize(nb_path)//1024} KB)")
