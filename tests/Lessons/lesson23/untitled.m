load('rx_after_1_sdr1.mat');
data = matrix_name;


ofdm = fft(data.')

figure;
imagesc(abs(ofdm));
figure;
plot(abs(fftshift(ofdm)));

ofdm = [ofdm(65:128,:);ofdm(1:64,:)];
%plot(abs(ofdm));
figure;
imagesc(abs(ofdm));