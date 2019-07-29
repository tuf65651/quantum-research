N = 27;
a = 2;

f_2_371 = f_mod(2,371);

%% Factor 15 with a=2
f_2_15 = f_mod(2,15);
R = brute_r_from_vec(f_2_15)

%% function

function mods = f_mod(a,N)
% assert a less than N
if a >= N
errID = "f_mod:InvalidInput";
errText = "a must be less than N";
ME = MException(errID,errText);
throw(ME);
end

% allocate vector for returns
mods = zeros(N,1);
% base
mods(1) = a;
    % iterate
    for i = 2:N
    dividend = a * mods(i-1);
    mods(i) = mod(dividend, N);
    end
end

function r = brute_r_from_vec(vec)
r=1;
while vec(r) ~= 1
    r = r + 1;
end
end
% 
% function r = mod_mod(dividend, divisor, prev)
% r = mod(prev * dividend, divisor);
% end