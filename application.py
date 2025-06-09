import pickle
from flask import Flask,request,jsonify,render_template
import numpy as np
import pandas as pd
import sympy
application=Flask(__name__)
app=application


@app.route('/',methods=['GET','POST'])
def profit():
    if request.method=='POST':
        f=request.form.get('functionInput')
        fxyz=sympy.sympify(f)
        g=request.form.get('constraintInput')
        gxyz=sympy.sympify(g)
        k,x,y=sympy.symbols('k x y')
        lhs=[sympy.diff(fxyz,x),sympy.diff(fxyz,y)]
        rhs=[sympy.diff(gxyz,x),sympy.diff(gxyz,y)]
        rhs=[k*i for i in rhs]
        eq1=sympy.Eq(lhs[0],rhs[0])
        eq2=sympy.Eq(lhs[1],rhs[1])
        eq1_x=sympy.solve(eq1,x)
        eq2_sub=eq2.subs({x:eq1_x[0]})
        set_k=sympy.solveset(eq2_sub,k)
        sol=[]
        set_y=set()
        for k_val in list(set_k):
            eq1_k=eq1.subs(k,k_val)
            eq_g=sympy.Eq(gxyz,0)
            eq1_x=sympy.solve(eq1_k,x)
            f_eq=eq_g.subs(x,eq1_x[0])
            solve_y=sympy.solveset(f_eq,y)
            for y_val in list(solve_y):
                x_val_eq=eq1_k.subs(y,y_val)
                x_val=sympy.solve(x_val_eq,x)
                sol.append((x_val[0],y_val))
        l_f=[]
        for item in sol:
            (a,b)=item
            l_f.append(fxyz.subs({x:a,y:b}))
        min_i=0
        for i,it in enumerate(l_f):
            if l_f[i]<l_f[min_i]:
                min_i=i
        max_i=0
        for i,it in enumerate(l_f):
            if l_f[i]>l_f[max_i]:
                max_i=i

        return render_template('index1.html',result=sol,max=sol[max_i],min=sol[min_i])

        





    else:
        return render_template('index1.html')


        
        

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)