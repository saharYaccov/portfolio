
# GUI Calculator

This script implements a versatile GUI calculator application using Tkinter, SymPy, NumPy, Matplotlib, PyAutoGUI, and other libraries. It supports standard arithmetic, scientific operations, symbolic derivatives & integrals, Taylor series plotting, polynomial solving, matrix determinants, complex number handling, base conversions, Riemann sums, 2D/3D plotting, and custom constants.

**Note:** This code was written before the AI revolution.

## Core Features

1. **Basic & Scientific Calculations**
   - Buttons for digits, operators (+, –, ×, ÷, %, ^)
   - Trigonometric functions (sin, cos, arctan) with Taylor-series approximations
   - Logarithm (ln), exponentials (eˣ), π constant insertion
   - Factorial via SciPy’s Gamma function
   - Nth-root extraction with user-specified root

2. **Symbolic & Numeric Analysis**
   - Numerical derivative at a user-given point using h→0 limit
   - Taylor series expansion and plotting for inputs containing ‘x’
   - 3D surface plotting of SymPy expressions via Matplotlib/sympy.plotting

3. **Polynomial & Matrix Solvers**
   - Quadratic and cubic equation solvers via SymPy
   - Determinant of 3×3 and 4×4 matrices with user prompts

4. **Complex Number Utilities**
   - Input complex numbers, extract real/imaginary parts
   - Polar form conversion (r·e^{iθ})

5. **Data & Plotting**
   - 2D function plotting
   - Riemann sum approximation of definite integrals
   - Automatic screen prompts for ranges, step sizes via PyAutoGUI

6. **Custom Constants**
   - Store up to three user-defined constants (A, B, C) and reuse in calculations

7. **User Interface**
   - Responsive Tkinter grid of buttons, real-time display updates
   - Pop-up dialogs for variable input, confirmation prompts

## Dependencies

- tkinter
- pyautogui
- sympy
- numpy
- scipy
- matplotlib
- keyboard
- bidi & arabic_reshaper (if RTL support needed)

<img width="416" height="261" alt="image" src="https://github.com/user-attachments/assets/5a56f18d-51f3-473c-9a16-62f28c069b7a" />


Run the script to launch the calculator window. Click buttons or use prompts for advanced operations.

@author: Sahar
