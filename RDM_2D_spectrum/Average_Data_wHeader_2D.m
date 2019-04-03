function [output,ptsperps]=Average_Data_wHeader(stringbase,numavg)
%% Function written by Marco A. Allodi and Ian Finneran
%% Function inputs%%%%%%%%%
%  stringbase is the file name as a matlab string without the number attached, 
%   ie. 'sample_scan_'
%
%  numavg is the number of files the function should average
%   when numavg is set to 0, the function will average every spectrum of 
%   that name in the folder. 
%% Begin Code

%Parse the file header to get the points per ps and the time window.
headerfile=strcat(stringbase,num2str(0),'1');
fid=fopen(headerfile,'r');
parse=textscan(fid,'%11s %8f %10s %3f');%set the numbers like %11s based on the size of the string

if fid > 0
    exist=1; %set while-loop condition variable
end

%parse is a cell with four columns of data. the first value in the ptsperps column and time_window column are the numbers we need.
%I'm not sure what else textscan gives us, but we can just grab the first value.
ptsperps=parse{1,2};ptsperps=ptsperps(1);
time_window=parse{1,4};time_window=time_window(1);
fclose(fid);
time_window=time_window-0.25;

%number of data points in a scan in our time window
points=round(time_window*ptsperps); 

%initilizing matricies
avg=zeros([1,points]);
cut_data=zeros([1,points]);

%initialize inputs for the first iteration of the while loop
k=0;
stringend=num2str(k);
filetoload=strcat(stringbase,stringend,'1');

%% Begin loops which will bring in the data.

%This condition will average all the files in a folder without specifying
%a number of averages.
if numavg==-1
    
    
   
    file=dlmread(filetoload,'\t',1,0); %pulls in a scan
    avg=file(:,2); %THz data 
    
%this loop pulls in all the individual scans up to numavg and computes the average.    
else
    for i=0:numavg
    i
    stringend=num2str(i);
    filetoload=strcat(stringbase,stringend,'1');
    file=dlmread(filetoload,'\t',1,0); %pulls in a scan
    data=file(:,1); %THz data 
    position=file(:,2); %delay position data
        %The number for steps by which we overshoot the start position
        %varies based on delayline speed and can be found by looking at a plot of the data in the position column
    

     [~, index]=min(abs(position-18)); %Find the point that corresponds to the start of the THz scan.
    
    %code added by Xander to replace the for loop. Somehow this is faster
    %in Matlab than building a matrix with a for loop.
    cut_data(1:points)=data(index:(index+points-1));
    avg=avg+cut_data;
        
    end
end

%% Finish Processing Data and Output Data.
l=length(avg);
time=linspace(0,1,l)*time_window;

if numavg~=0
   avg=fliplr((avg/numavg));%flips the timing axis to the standard
% avg=moving_average(avg,1);%boxcars the data, 1 pt on either side
end

if numavg==0
   avg=fliplr((avg/(k-1)));%flips the timing axis to the standard 
end

output(:,1)=time;
output(:,2)=avg;


end