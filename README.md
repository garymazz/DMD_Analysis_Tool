# DMD Analysis Tool

A modular CLI framework built on [Cement](https://builtoncement.com/) and [Pydantic](https://docs.pydantic.dev/) for analyzing DMD system data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Module API](#module-api)
- [Developer Guide: Creating New Modules](#developer-guide-creating-new-modules)

---

## Installation

1. **Unzip the archive:**
   ```bash
   unzip dmd_tool_manual_help_fix.zip
   cd dmd_tool_manual_help_fix
   ```

2. **Install Dependencies:**
   ```bash
   pip install cement pandas rich pydantic openpyxl odfpy pyarrow matplotlib
   ```

---

## Usage

**List Commands:**
```bash
python main.py --help
```

**Run an Analysis:**
```bash
python main.py analyze_series --input data.csv --min-stack 3 --output results.csv
```

**View Full Parameter Registry:**
```bash
python main.py --help-detail
```

---

## Architecture

The tool follows a **Controller-Service-Model** pattern, adapted for a CLI environment.

### 1. Core Framework (`core/`)
*   **`app.py`**: Initializes the Cement App, sets up the `Rich` console, and handles global help overrides.
*   **`controllers.py`**: Defines `BaseOperationController`, which all operations must inherit from. It handles the binding between Cement's argument parsing and Pydantic's validation.

### 2. Models (`models/`)
*   **`analysis_schema.py`**: Contains Pydantic V2 models. These define the "contract" for every operation. Arguments defined here are automatically converted into CLI flags.

### 3. Operations (`operations/`)
*   Each file (e.g., `analyze_series.py`) represents a single CLI sub-command.
*   They contain **only** the orchestration logic: getting parameters, calling the library functions, and printing results.

### 4. Library (`lib/`)
*   Pure Python functions containing the business logic.
*   **`data_loaders.py`**: Robust file I/O (CSV, Parquet, Excel).
*   **`filters.py`**: Pandas logic for system error filtering.
*   **`statistics.py`**: Mathematical algorithms (e.g., contiguous stack detection).
*   **`plotting.py`**: Visualization logic.

---

## Module API

### `BaseOperationController`
Located in `core/controllers.py`.

*   **`Meta.label`** *(str)*: The CLI command name (e.g., `analyze_series`).
*   **`Meta.description`** *(str)*: Short summary shown in `main.py --help`.
*   **`Meta.help_detailed`** *(str)*: Long description shown in `main.py --help-detail`.
*   **`Meta.param_model`** *(Type[BaseModel])*: The Pydantic model class defining the arguments.
*   **`Meta.arguments`** *(list)*: Cement-style argument definitions (Must match fields in `param_model`).
*   **`execute(self)`**: The method called when the command is run. Use `self.get_params()` to retrieve validated arguments.

---

## Developer Guide: Creating New Modules

**Prompt for LLMs:**
*"Create a new DMD Operation module that [Function Description]. Follow the v34 Architecture."*

### Step-by-Step Implementation Guide

#### 1. Define the Parameters (Model)
Open `models/analysis_schema.py` and add a new class inheriting from `BaseAnalysisParams`.

```python
class MyNewOpParams(BaseAnalysisParams):
    threshold: float = Field(0.5, description="Sensitivity threshold.")
    # 'input_file' is already inherited
```

#### 2. Create the Operation Controller
Create a new file `operations/my_new_op.py`.

```python
from core.controllers import BaseOperationController
from models.analysis_schema import MyNewOpParams
from lib import filters  # Import reusable logic

class MyNewOpController(BaseOperationController):
    class Meta:
        label = '--my_new_op'
        description = "Short summary of the op."
        help_detailed = "Longer explanation of what logic is applied."
        param_model = MyNewOpParams

        # Define CLI arguments (Must match Pydantic fields)
        arguments = [
            (['--input'], {'help': 'Input file', 'dest': 'input_file'}),
            (['--threshold'], {'help': 'Sensitivity', 'type': float, 'default': 0.5, 'dest': 'threshold'}),
        ]

    def _default(self):
        # 1. Get Validated Parameters
        params = self.get_params() 

        # 2. Use Lib functions (Do not write complex math here)
        self.app.console.print(f"Analyzing {params.input_file} with T={params.threshold}...")
        df = filters.load_raw_df(params.input_file)

        # 3. Output Results
        self.app.console.print(f"Found {len(df)} rows.")
```

#### 3. Register the Module
Open `main.py` and add the new controller to the registration list.

```python
from operations.my_new_op import MyNewOpController

# ... inside the list ...
for c in [..., MyNewOpController]:
    DMDFramework.Meta.handlers.append(c)
```
