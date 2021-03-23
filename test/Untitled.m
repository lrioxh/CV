%Edge linking using local processing
clc;
clear all;
close all;
%边缘连接测试图像
I=im2double(imread('D:\file\class\cv\code\images\4Fig1027(a)(van_original).tif'));
[M,N]=size(I);
%=============================边缘检测(六)=================================
% Edge linking using local processing
%边缘连接的局部处理
%--------------------------计算图像梯度和角度------------------------------
n_l=1;
%Sobel算子
s_y=[-1 -2 -1;
    0 0 0;
    1 2 1];
s_x=[-1 0 1;
    -2 0 2;
    -1 0 1];
%定义梯度和角度
gx=zeros(M,N);
gy=zeros(M,N);
f_pad=padarray(I,[n_l,n_l],'replicate');
for i=1:M
    for j=1:N
        Block=f_pad(i:i+2*n_l,j:j+2*n_l);
        gx(i,j)=sum(sum(Block.*s_x));
        gy(i,j)=sum(sum(Block.*s_y));        
    end
end
gx=abs(gx);
gy=abs(gy);
% M_s=sqrt(gx.^2+gy.^2);
% M_s=M_s/max(M_s(:));
a_s=atan2(gy,gx)*180/pi;
% imshow(M_s)
%-------------------------------图像二值化---------------------------------
%设置梯度门限
th=0.3;
T_max=max(gy(:));
T_M=T_max*th;
T_A=45;
%计算水平方向
Tx=zeros(M,N);
A_x=90;
for i=1:M
    for j=1:N
        if gy(i,j)>T_M
            if a_s(i,j)>=A_x-T_A && a_s(i,j)<=A_x+T_A
                Tx(i,j)=1;
            end
        end
    end
end
 
T_max=max(gx(:));
T_M=T_max*th;
T_A=45;
Ty=zeros(M,N);
A_y=0;
for i=1:M
    for j=1:N
        if gx(i,j)>T_M
            if a_s(i,j)>=A_y-T_A && a_s(i,j)<=A_y+T_A
                Ty(i,j)=1;
            end
        end
    end
end
 
%-----------------------------填充空当-------------------------------------
L=25;
%水平二值图像沿x方向进行扩展
Tx_pad=padarray(Tx,[0,L-1],'post');
Tx_g=zeros(M,N);
for i=1:M
    for j=1:N
        if Tx_pad(i,j)==1 && Tx_pad(i,j+1)==0
            Block=Tx_pad(i,j+2:j+L-1);
            ind=find(Block==1);
            if ~isempty(ind)                
                ind_Last=j+2+ind(1,length(ind))-1;
                Tx_pad(i,j:ind_Last)=1;
                Tx_g(i,j:ind_Last)=1;
            end
        else
            Tx_g(i,j)=Tx_pad(i,j);
        end
    end
end
%沿垂直方向进行填充
Ty_pad=padarray(Ty,[L-1,0],'post');
Ty_g=zeros(M,N);
for j=1:N
    for i=1:M
        if Ty_pad(i,j)==1 && Ty_pad(i+1,j)==0
            Block=Ty_pad(i+2:i+L-1,j);
            ind=find(Block==1);
            if ~isempty(ind)                
                ind_Last=i+2+ind(length(ind),1)-1;
                Ty_pad(i:ind_Last,j)=1;
                Ty_g(i:ind_Last,j)=1;
            end
        else
            Ty_g(i,j)=Ty_pad(i,j);
        end
    end
end
T_g=Ty_g+Tx_g;
[g]=ImageThinning(T_g);
imshow(g)