- arithmetic-arranger：算式格式化
  - Example：curl http://127.0.0.1:31128/function/arithmetic-arranger.openfaas-fn-pyz --data-binary '{"problems":["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]}'

- curve-fitting：线性拟合
  - curl http://127.0.0.1:31128/function/curve-fitting.openfaas-fn-pyz --data-binary '{"X":[150, 200, 250, 350, 300, 400, 600],"y":[6450, 7450, 8450, 9450, 11450, 15450, 18450]}'

- eigen：求解矩阵特征值和特征向量
  - curl http://127.0.0.1:31128/function/eigen.openfaas-fn-pyz --data-binary '{"matrix":[[-1, 1, 0],[-4, 3, 0],[1, 0, 2]]}'

- linear-programming：线性规划求解
  - Example：curl http://127.0.0.1:31128/function/linear-programming.openfaas-fn-pyz --data-binary '{"MinOrMax":"min","target":[-1,4],"A":[[-3,1],[1,2]],"b":[6,4],"bounds":[[null,null],[-3,null]]}'

- prob-calculator：计算古典概型概率
  - curl http://127.0.0.1:31128/function/prob-calculator.openfaas-fn-pyz --data-binary '{"hat":{"blue":4,"red":2,"green":6},"expected_balls":{"blue":2,"red":1},"num_balls_drawn":4,"num_experiments":3000}'

- time-calculator：日期计算
  - curl http://127.0.0.1:31128/function/time-calculator.openfaas-fn-pyz --data-binary '{"start":"11:06 PM","duration":"2:02"}'