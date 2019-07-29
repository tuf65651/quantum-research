%% Set CX_10
CX_10 = H2 * CX_01 * H2;

%% Begin Grover's - superposition
circuit = H2 * ket_00

%% Oracle - f(w) is CZ(10)(w)
circuit = H1_0 * circuit;
circuit = CX_10 * circuit;
circuit = H1_0 * circuit

%% Grover Diffusion
% Flip Ys to Zs
circuit = H2 * circuit;
% Flip Zs to -Zs
circuit = kron(X, X) * circuit;

% CZ(0 to 1)
circuit = H1_0 * circuit;
circuit = CX_10 * circuit;
circuit = H1_0 * circuit;

% Flip Zs to -Zs
circuit = kron(X, X) * circuit; 
% Flip Ys to Zs
circuit = H2 * circuit;

%% Measure
disp(circuit)