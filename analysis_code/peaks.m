clear;

pkg load control;
pkg load signal;

[data1, sampRate] = audioread('song.wav');

pLength = 735;

fStart = (pLength * 500) + 1;
fEnd   = (pLength * 501) + 1;

posCurrent = fStart;

vP = [];

while posCurrent < fEnd
  if data1(posCurrent) > 0
    vP = vertcat(vP, data1(posCurrent));
  endif
  posCurrent += 1;
endwhile

# Find the peaks
[pks idx] = findpeaks(vP);

#r = 1:length(vP);
r = fStart:fEnd;

spot = 1:(length(idx));
s = 1:length(vP);
#plot(r, data1(r));#, r(idx), pks(idx));
plot(s, fStart*vP(s), s(idx), fStart*pks(spot));




#plot(r, vP(r));

# Find only the positive values

