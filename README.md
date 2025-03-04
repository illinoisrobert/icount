# icount
Python lib to query `/proc/interrupts`

## Usage

#### Install 
```sh
pip install git+https://github.com/illinoisrobert/icount.git@v0.1
```

#### Program
```python
import icount
from pprint import pprint

pprint(list(icount.snapshot("wifi")))
```

#### Output
```
[{'Device': 'iwlwifi',
  'Edge': '0-edge',
  'IRQ': '152:',
  'PerCPU': [3205894, 0, 0, 0, 0, 0, 980976, 0],
  'Total': 4186870,
  'Type': 'IR-PCI-MSI-0000:02:00.0'}]
```

## Copying

Copyright 2025, The Board of Trustees of the University of Illinois
See [LICENSE](LICENSE) for details.
