from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# 创建量子寄存器
q = QuantumRegister(8, 'q')
c = ClassicalRegister(5, 'c')  # 控制寄存器
qc = QuantumCircuit(q, c)

qc.h(q[1])  # 对第一个量子比特应用Hadamard门
qc.h(q[2])
qc.h(q[3])

sub_r_0 = QuantumCircuit(1, name='R\\_0')
R_0 = sub_r_0.to_gate()
c_R_0 = R_0.control(1, ctrl_state='0')
qc.append(c_R_0, [q[1], q[0]])

sub_r_1 = QuantumCircuit(1, name='R\\_1')
R_1 = sub_r_1.to_gate()
c_R_1 = R_1.control(2, ctrl_state='10')
qc.append(c_R_1, [q[1], q[5], q[0]])

sub_r_2 = QuantumCircuit(1, name='R\\_2')
R_2 = sub_r_2.to_gate()
c_R_2 = R_2.control(2, ctrl_state='11')
qc.append(c_R_2, [q[1], q[5], q[0]])

sub_r_3 = QuantumCircuit(1, name='R\\_3')
R_3 = sub_r_3.to_gate()
c_R_3 = R_3.control(4, ctrl_state='1000')
qc.append(c_R_3, [q[1], q[5], q[6], q[7], q[0]])

sub_m_2 = QuantumCircuit(4, name='M\\_2')
M_2 = sub_m_2.to_gate()
c_M_2 = M_2.control(2, ctrl_state='00')
qc.append(c_M_2, [q[1], q[2], q[4], q[5], q[6], q[7]])

sub_l = QuantumCircuit(3, name='L')
L_gate = sub_l.to_gate()
controlled_L = L_gate.control(3, ctrl_state='001')
qc.append(controlled_L, [q[1], q[2], q[3], q[5], q[6], q[7]])

sub_r = QuantumCircuit(3, name='R')
R_gate = sub_r.to_gate()
controlled_R = R_gate.control(3, ctrl_state='011')
qc.append(controlled_R, [q[1], q[2], q[3], q[5], q[6], q[7]])

sub_d_2 = QuantumCircuit(4, name='D\\_2')
D_2 = sub_d_2.to_gate()
c_D_2 = D_2.control(2, ctrl_state='01')
qc.append(c_M_2, [q[1], q[2], q[4], q[5], q[6], q[7]])

qc.h(q[1])
qc.h(q[2])
qc.h(q[3])

# 测量量子比特
for i in range(5):
    qc.measure(q[i], c[i])

qc.draw('latex_source', filename='example.tex')
