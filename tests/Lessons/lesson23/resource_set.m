load('rx_before_2_sdr1.mat');
data = matrix_name;
load('pss_time.mat');
pss = matrix_name;
pss_reg = matrix_name;


corr_pss=abs(filter(flip(conj(pss)),1,data));
c= max(corr_pss);
figure;
plot(abs(corr_pss));
corr_pss = corr_pss ./ c;
max_cor = find(corr_pss > 0.9)


%data33 = data(539:1499);
data_cor = data(max_cor(1):end);

frame = 10;

test = data_cor(1:960*frame);
%data = data(1:1920*2)





data33 = reshape(test,160,6*frame).' ;

data3 = data33(:, 33:end);
%data1= data1(33:end);
%data2= data2(33:end);



ofdm = fft(data3.');
%ofdm2 = fft(data2.');

scatt = [ofdm(2, :), ofdm(3, :),ofdm(8, :),ofdm(9, :),ofdm(14, :),ofdm(15, :)]
%scatterplot(scatt)


%figure;
%imagesc(abs(ofdm));

%ofdm1 = [ofdm(65:128,:);ofdm(1:64,:)];
%plot(abs(ofdm));
ofdm2 = [ofdm(65:128,:);ofdm(1:64,:)];
figure;
imagesc(abs(ofdm2));
figure;
plot(abs(ofdm2));

corr_pss=filter(flip(conj(pss)),1,data);
%figure;
%plot(abs(corr_pss));
corr_coef = flip(conj(pss_reg));
%data=matrix_name;
L = length(pss_reg);
partA = filter(corr_coef(1:(L/2)),1,data);
xDelayed = [zeros(1,L/2), data(1:end-(L/2))];
partB = filter(corr_coef((L/2)+1:end),1,xDelayed);
correlation= abs(partA + partB);
phaseDiff = partA .* conj(partB);
%figure;
%plot(correlation);
%yyaxis 'right'
%figure;
%plot(angle(phaseDiff));
%hold off;
phaseDiff_max=phaseDiff(find(correlation>2e6));
m = 15000;
CFO = angle(phaseDiff_max)/(pi*1/m);
istart = find(correlation==max(correlation));

CFO_max = angle(phaseDiff(istart))/(pi*1/m);
count = length(test);

t = 1:count ;
t = t/1920000; %период дискритизации

test_1 = test .* exp(-1i *2*pi*conj(CFO_max)*t);

save("freq.mat", "test_1", "-mat")
data33 = reshape(test_1,160,6*frame).';

data3 = data33(:, 33:end);

ofdm = fft(data3.');
%ofdm2 = fft(data2.');

scatt = [ofdm(2, :), ofdm(3, :),ofdm(8, :),ofdm(9, :),ofdm(14, :),ofdm(15, :)];
scatterplot(scatt);


%figure;
%imagesc(abs(d0));

ofdm2 = [ofdm(65:128,:);ofdm(1:64,:)];
%plot(abs(ofdm));
figure;
plot(abs(ofdm2));
figure;
imagesc(abs(ofdm2));
