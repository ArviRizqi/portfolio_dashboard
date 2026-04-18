import os
import glob
import re

pattern1 = r'import os, sys(?:, warnings)?\s*(warnings\.filterwarnings\("ignore"\)\s*)?sys\.path\.insert\(0, os\.path\.join\(os\.path\.dirname\(__file__\), "\.\./\.\./\.\./"\)\)'
replacement1 = r'''import sys
from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import os'''

files = glob.glob(r'e:\Python Project\portfolio_dashboard\projects\*\pages\*.py')
for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace imports and sys.path.insert
    # Let's do it with string replace since regex might miss some spaces.
    content = content.replace(
        'import os, sys\nsys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))',
        'import sys, os\nfrom pathlib import Path\nCURRENT_DIR = Path(__file__).resolve().parent\nPROJECT_ROOT = CURRENT_DIR.parent.parent.parent\nif str(PROJECT_ROOT) not in sys.path:\n    sys.path.insert(0, str(PROJECT_ROOT))'
    )
    content = content.replace(
        'import os, sys, warnings\nwarnings.filterwarnings("ignore")\n\nsys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))',
        'import sys, os, warnings\nwarnings.filterwarnings("ignore")\nfrom pathlib import Path\nCURRENT_DIR = Path(__file__).resolve().parent\nPROJECT_ROOT = CURRENT_DIR.parent.parent.parent\nif str(PROJECT_ROOT) not in sys.path:\n    sys.path.insert(0, str(PROJECT_ROOT))'
    )

    # 2. Replace BASE and os.path.join paths
    content = content.replace('BASE      = os.path.dirname(__file__)', 'BASE = str(CURRENT_DIR)')
    content = content.replace('BASE       = os.path.dirname(__file__)', 'BASE = str(CURRENT_DIR)')
    content = content.replace('BASE = os.path.dirname(__file__)', 'BASE = str(CURRENT_DIR)')
    
    content = content.replace('os.path.dirname(__file__)', 'str(CURRENT_DIR)')

    # We need to make sure we don't have multiple CURRENT_DIR definitions if we replaced it many times.
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")
