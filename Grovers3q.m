%% Set 3D kets
ket_000 = kron(ket_00, ket_0);
ket_001 = kron(ket_00, ket_1);
ket_010 = kron(ket_01, ket_0);
ket_011 = kron(ket_01, ket_1);
ket_100 = kron(ket_10, ket_0);
ket_101 = kron(ket_10, ket_1);
ket_110 = kron(ket_11, ket_0);
ket_111 = kron(ket_11, ket_1);

kets_3q = [ket_000 ket_001 ket_010 ket_011 ket_100 ket_101 ket_110 ket_111]

% %% Set CX gates
% CX_10 = H2 * CX_01 * H2;
% CX3_10 = kron(CX_10, eye(2));
% CX3_20 = 

%% Begin 3-qubit circuit in superposition
circuit = H3 * ket_000

%% Oracle CCZ(1,2,0)

CCZ = kron(T, eye(4)) * CX3_20 * kron(conj(T), eye(4)) * CX3_10;
CCZ = CX3_20 * kron(conj(T), eye(4)) * CX3_10 * CCZ;
CCZ = kron(kron(conj(T), conj(T)), eye(2)) * CCZ; % rotate first two qubits
CCZ = kron(kron(eye(2), conj(T)), eye(2)) * CCZ;
CCZ = kron(eye(2), CX_10) * CCZ; % CNOT(1 if 2)
CCZ = kron( kron(eye(2), conj(T)), eye(2) ) * CCZ;
CCZ = kron(eye(2), CX_10) * CCZ;
CCZ = kron(eye(4), T) * CCZ;


circuit = CCZ * circuit

%% Grover's

circuit = circuit