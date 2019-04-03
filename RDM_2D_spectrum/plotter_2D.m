function [ output_args ] = plotter_2D( data_matrix )


[M,I] = max(data_matrix(:));
[I_row, I_col] = ind2sub(size(data_matrix),I);

0.05*I_col
0.05*I_row
a = size(data_matrix);


v = 0:.1:1;
figure('position', [100, 100, 800, 400]);
[C,h] = contourf([1:a(1)]*0.05-1.2+50*.05,[1:a(2)]*0.05-1.55+0*.05,data_matrix.',10)

%[C,h] = contourf([1:a(1)]*0.05-0.05*I_row,[1:a(2)]*0.05-0.05*I_col,data_matrix.',10);
set(h,'LineColor','none');
set(gca,'FontSize',12);
axis equal
xlabel('t2 (ps)') % x-axis label
ylabel('t1 (ps)') % y-axis label
end