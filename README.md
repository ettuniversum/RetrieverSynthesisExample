# RetrieverSynthesisExample
Example of a retriever and synthesis response without embedding or vector index. Optimized for performance

Expected outcome:

if(xC0.c[0] == xC0.c[2]) {
            double b = 0.5*xC0.c[1]/xC0.c[0];
            double c = xC0.c[2]/xC0.c[0];
            //assert(fabs(b*b-c) > 1e-10);
            double d =  std::sqrt(b*b-c);
            //assert(fabs(b-d) > 1e-10);
            n0 = Point(1, b+d);
            n1 = Point(1, b-d);
        } else if(fabs(xC0.c[0]) > fabs(xC0.c[2])) {
            double b = 0.5*xC0.c[1]/xC0.c[0];
            double c = xC0.c[2]/xC0.c[0];
            //assert(fabs(b*b-c) > 1e-10);
            double d =  std::sqrt(b*b-c);
            //assert(fabs(b-d) > 1e-10);
            n0 = Point(1, b+d);
            n1 = Point(1, b-d);
        } else {
            double b = 0.5*xC0.c[1]/xC0.c[2];
            double c = xC0.c[0]/xC0.c[2];
            //assert(fabs(b*b-c) > 1e-10);
            double d =  std::sqrt(b*b-c);
            //assert(fabs(b-d) > 1e-10);
            n0 = Point(b+d, 1);
            n1 = Point(b-d, 1);
        }

        Line L0 = Line::from_origin_and_vector(B0, rot90(n0));
        Line L1 = Line::from_origin_and_vector(B0, rot90(n1));

        std::vector<double> rts = C1.roots(L0);
        for(double rt : rts) {
            Point P = L0.pointAt(rt);
            res.push_back(P);
        }
        rts = C1.roots(L1);

---------------------

Seconds: 8.031922340393066
The vulnerability is caused by the use of a shadowed local variable `b` in the function `decompose_degenerate`. The variable `b` is declared twice, once as a local variable inside the `if` statement and again as a parameter to the `std::sqrt` function. This can lead to unexpected behavior, as the value of `b` used by the `std::sqrt` function may not be the same as the value of `b` used in the `if` statement.

In this specific case, the vulnerability is caused by the fact that the `std::sqrt` function takes a double argument and returns its square root. However, the value passed to the function is the result of dividing two integers, which may not be exactly representable as a floating-point number. As a result, the value of `b` used in the `if` statement may not be the same as the value of `b` used by the `std::sqrt` function, leading to unexpected behavior.

To fix this vulnerability, the code should use a different variable name for the local variable declared inside the `if` statement, or it should use a different function that does not require the use of a shadowed local variable.
