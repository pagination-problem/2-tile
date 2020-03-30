\ENCODING=ISO-8859-1
\Problem name: [3, 3, 3, 4]

Minimize
 obj1: - x_1a - x_1b - x_1c - x_1d - x_1e - x_1f
Subject To
 c1:  x_1a - x_2a + x_1b - x_2b + x_1c - x_2c + x_1d - x_2d + x_1e - x_2e
      + x_1f - x_2f <= 0
 c2:  x_1a + x_2d <= 1
 c3:  x_2a + x_1d <= 1
 c4:  x_1b + x_2d <= 1
 c5:  x_2b + x_1d <= 1
 c6:  x_1c + x_2d <= 1
 c7:  x_2c + x_1d <= 1
 c8:  x_1d + x_2e <= 1
 c9:  x_2d + x_1e <= 1
 c10: x_1e + x_2f <= 1
 c11: x_2e + x_1f <= 1
 c12: x_1a + x_2a <= 1
 c13: x_1b + x_2b <= 1
 c14: x_1c + x_2c <= 1
 c15: x_1d + x_2d <= 1
 c16: x_1e + x_2e <= 1
 c17: x_1f + x_2f <= 1
Bounds
 0 <= x_1a <= 1
 0 <= x_2a <= 1
 0 <= x_1b <= 1
 0 <= x_2b <= 1
 0 <= x_1c <= 1
 0 <= x_2c <= 1
 0 <= x_1d <= 1
 0 <= x_2d <= 1
 0 <= x_1e <= 1
 0 <= x_2e <= 1
 0 <= x_1f <= 1
 0 <= x_2f <= 1
Binaries
 x_1a  x_2a  x_1b  x_2b  x_1c  x_2c  x_1d  x_2d  x_1e  x_2e  x_1f  x_2f 
End
