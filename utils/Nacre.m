% housekeeping
close all
clear all
clc

% init
% grid on
hold on
axis square

x=[2 3 4 5 6 7 8 9; 5.5 5.5 5.5 5.5 5.5 5.5 5.5 5.5];
y=[2 2 2 2 2 2 2 2; 6 6 6 6 6 6 6 6];
z=[4 4 4 4 4 4 4 4 ; 2 2 2 2 2 2 2 2 ];

x=[x, [10 11 12 13 14 15 16 17; 13.5 13.5 13.5 13.5 13.5 13.5 13.5 13.5]];
x=[x, [18 19 20 21 22 23 24 25; 21.5 21.5 21.5 21.5 21.5 21.5 21.5 21.5]];

y=[y, y, y];
z=[z, z, z];

% for other side
x=[x,x];
y=[y,y];
zOther = z;
zOther(2,:)=zOther(2,:)+4;
z=[z,zOther];


x=[x,8.+x];
y=[y,y];
z=[z,z];

x=[x, x];
y=[y, flipud(y+14)];
z=[z, z];


scatterX=unique(x(1,:));
scatterX=[scatterX scatterX];
scatterY=ones(1,32).*20;
scatterY=[scatterY scatterY-18];
scatterZ=ones(1,64).*4;

% switches
swX=unique(x(2,:));
swX=[[swX;swX(1) swX(1) swX(1) swX(1)],[swX;swX(2) swX(2) swX(2) swX(2)],[swX;swX(3) swX(3) swX(3) swX(3)],[swX;swX(4) swX(4) swX(4) swX(4)]];
swY=[[6 6 6 6; 16 16 16 16],[6 6 6 6; 16 16 16 16],[6 6 6 6; 16 16 16 16],[6 6 6 6; 16 16 16 16]];
swZ=[[2 2 2 2; 2 2 2 2],[2 2 2 2; 2 2 2 2],[2 2 2 2; 2 2 2 2],[2 2 2 2; 2 2 2 2]];

swX=[swX,swX];
swY=[swY,swY];
swZ=[swZ,(swZ+4)];


scatterSwX=unique(x(2,:));
scatterSwX=[scatterSwX, scatterSwX];
scatterSwY=[6 6 6 6 16 16 16 16];
scatterSwZ=[6 6 6 6 6 6 6 6];
scatterSwX=[scatterSwX, scatterSwX];
scatterSwY=[scatterSwY,scatterSwY];
scatterSwZ=[scatterSwZ,scatterSwZ-4];

% cores
scatterCoreX=[2.8750    4.6250    6.3750    8.1250];
scatterCoreX=[scatterCoreX, scatterCoreX+8, scatterCoreX+16, scatterCoreX+24];
scatterCoreX = [scatterCoreX,scatterCoreX];
scatterCoreY=[6 6 6 6];
scatterCoreY=[scatterCoreY,scatterCoreY,scatterCoreY,scatterCoreY];
scatterCoreY = [scatterCoreY,scatterCoreY+10];
scatterCoreZ=[12 12 12 12];
scatterCoreZ=[scatterCoreZ,scatterCoreZ,scatterCoreZ,scatterCoreZ];
scatterCoreZ = [scatterCoreZ,scatterCoreZ];

scatterCoreX=[scatterCoreX, scatterCoreX];
scatterCoreY=[scatterCoreY, scatterCoreY];
scatterCoreZ=[scatterCoreZ, scatterCoreZ-16];


coreX = [5.5,5.5,5.5,5.5;2.8750    4.6250    6.3750    8.1250];
coreX=[coreX,coreX+8,coreX+16,coreX+24];
coreX=[coreX,coreX];
coreY= [6 6 6 6;6 6 6 6];
coreY = [coreY,coreY,coreY,coreY];
coreY=[coreY,coreY+10];
coreZ = [6 6 6 6; 12 12 12 12];
coreZ = [coreZ,coreZ,coreZ,coreZ];
coreZ = [coreZ,coreZ];

coreX=[coreX,coreX];
coreY=[coreY,coreY];
coreZ = [coreZ, flipud(coreZ)-10];
hold on

plot3(x,y,z,'LineWidth',1)
scatter3(scatterX,scatterY,scatterZ,'O','LineWidth',5,'MarkerFaceColor','r')


plot3(swX,swY,swZ,'LineWidth',2)
scatter3(scatterSwX,scatterSwY,scatterSwZ,'X','LineWidth',30,'MarkerFaceColor','g')

plot3(coreX,coreY,coreZ,'LineWidth',3)
scatter3(scatterCoreX,scatterCoreY,scatterCoreZ,'O','LineWidth',13,'MarkerFaceColor','b')

% % plot all pods
% for i=1:16
%     
%     plot3(x,y+(i-1)*25,z,'o')
%     plot3(x,y+(i-1)*25,z)
%     plot3(swX,swY,swZ,'--')
%     plot3(swX,swY+(i-1)*25,swZ,'LineWidth',2)
%     
% end

