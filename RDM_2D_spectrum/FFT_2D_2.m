function [ output_args ] = FFT_2D_2( data_matrix_cut )






x_max_cutoff=10;%in THz
x_min_cutoff=0;%in THz
y_max_cutoff=10;%in THz
y_min_cutoff=-10;%in THz


t1_time_spacing = 0.05000;
pointsperps=20;%2998
t3_time_spacing = 1/pointsperps;

%Generating the 2D apodization function 4/2/14 MAA
[m,n] = size(data_matrix_cut);
apod_x = hann(n); %standard Matlab Hann apodization
nwindow=round(n/2);
datatowindow=data_matrix_cut(:,nwindow);
apod_y = CosineWindowTHz(datatowindow); % asymetric Hann apodization for THz
%apod_y = zeros(m,1)+1;
apodization_matrix = apod_y*apod_x'; %outer product generates the apod matrix

%multiply by apodization function and take FFT
data_matrix_apod = data_matrix_cut;%.*apodization_matrix;
data_matrix_FFT = fft2(data_matrix_apod,1024,1024);%4096 is zeropadding. 



data_matrix_FFT_shift = fftshift((abs(data_matrix_FFT))); %putting zero in the center of the array

sizematrix = size(data_matrix_FFT_shift);
sizematrix = [sizematrix(1)-1 sizematrix(2)-1];
y_axis = [((-sizematrix(1)/2:sizematrix(1)/2))*((1/t3_time_spacing)/sizematrix(1))];
x_axis = [((-sizematrix(2)/2:sizematrix(2)/2))*((1/t1_time_spacing)/sizematrix(2))];



size(x_axis);
size(y_axis);

v = 0:0.00001:0.0001;

[ ~, x_index_cut_min] = min(abs(x_axis-x_min_cutoff));
[~, x_index_cut_max ]= min(abs(x_axis-x_max_cutoff));
[~, y_index_cut_min ] = min(abs(y_axis-y_min_cutoff));
[ ~, y_index_cut_max] = min(abs(y_axis-y_max_cutoff));
figure('position', [100, 100, 800, 400]);
%subplot(3,3,[4:5,7:8]);
data_matrix_FFT_cut = data_matrix_FFT_shift(y_index_cut_min:y_index_cut_max,x_index_cut_min:x_index_cut_max);
contourf(y_axis(y_index_cut_min:y_index_cut_max),x_axis(x_index_cut_min:x_index_cut_max),data_matrix_FFT_cut.',15)%,v)
set(gca,'FontSize',12)
%caxis([-100, 100])
y_axis_t = (-sizematrix(1)/2:sizematrix(1)/2)*t3_time_spacing;
x_axis_t = (-sizematrix(2)/2:sizematrix(2)/2)*t1_time_spacing;
x_axis_t = x_axis_t-2.85;
y_axis_t = y_axis_t+5.9;
refline(1,0)
refline(0,0)

xlabel('Probe Frequency (THz)') % x-axis label
ylabel('Pump Frequency (THz)') % y-axis label
axis([y_min_cutoff y_max_cutoff x_min_cutoff x_max_cutoff ])
%h = subplot(3,3,[1,2]);
%plot(finalspec(:,1),finalspec(:,2),'LineWidth',2);
%axis([0 5.5 0 10])
%ylabel('\alpha (cm^{-1})') % y-axis label
%set(gca,'XTickLabel',[]);
%can toggle on and off to save file.
%save('GABA_2D_FFT++','data_matrix_FFT_cut');

%a = subplot(3,3,[6,9]);
%plot(finalspec(:,2),finalspec(:,1),'LineWidth',2);
%axis([0 10 0 5.5])
%set(gca,'YTickLabel',[]);
%xlabel('\alpha (cm^{-1})') % y-axis label
%v_t = -.05:.001:.05;
%figure
%contourf(x_axis_t,y_axis_t,data_matrix,v_t,'LineStyle','none')
%xlabel('t1 (ps)')
%ylabel('t3 (ps)')


[M,I] = max(data_matrix_FFT_cut(:));
[I_row, I_col] = ind2sub(size(data_matrix_FFT_cut),I);

figure;
set(gca,'FontSize',12);
plot(y_axis(y_index_cut_min:y_index_cut_max),data_matrix_FFT_cut(:,I_col),'LineWidth',2);
hold all
plot(x_axis(x_index_cut_min:x_index_cut_max),data_matrix_FFT_cut(I_row,:),'LineWidth',2);
xlabel('Frequency (THz)') % x-axis label
ylabel('Intensity (Arb. Units)') % y-axis label
legend('Probe Axis','Pump Axis')


end

