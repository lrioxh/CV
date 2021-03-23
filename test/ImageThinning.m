%图像细化,目前只对二值图像进行处理
function [g]=ImageThinning(I)
n_l=1;
%对边界图进行扩充，四周各加1行、1列0（与结构元素的大小相对应），目的是为了处理边界点
I_pad=padarray(I,[n_l,n_l]);
%获得扩充图像大小
[M,N]=size(I_pad);
%寻找图像中的亮点，即值为1的点
ind=find(I_pad==1);
ind_c=[];
while ~isequal(ind_c,ind)
    %备份赋值，以便下一次循环开始进行比较
    ind_c=ind;
    %保存ind中符合条件的下标
    ind_sub=[];
    %按照B1结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p+1)) && ~isempty(find(ind==p-M+1)) && ~isempty(find(ind==p+M+1)) &&...
                isempty(find(ind==p-1)) && isempty(find(ind==p-M-1)) && isempty(find(ind==p+M-1))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    %将下标符合条件的数值，从ind中清除，以下类似
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end
    ind_sub=[];
    %按照B2结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p+1)) && ~isempty(find(ind==p-M)) && ~isempty(find(ind==p-M+1)) &&...
                isempty(find(ind==p-1)) && isempty(find(ind==p+M)) && isempty(find(ind==p+M-1))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end   
    ind_sub=[];
    %按照B3结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p-M-1)) && ~isempty(find(ind==p-M)) && ~isempty(find(ind==p-M+1)) &&...
                isempty(find(ind==p+M-1)) && isempty(find(ind==p+M)) && isempty(find(ind==p+M+1))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end
    ind_sub=[];
    %按照B4结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p-1)) && ~isempty(find(ind==p-M)) && ~isempty(find(ind==p-M-1)) &&...
                isempty(find(ind==p+1)) && isempty(find(ind==p+M)) && isempty(find(ind==p+M+1))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end    
    ind_sub=[];
    %按照B5结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p-M-1)) && ~isempty(find(ind==p-1)) && ~isempty(find(ind==p+M-1)) &&...
                isempty(find(ind==p-M+1)) && isempty(find(ind==p+1)) && isempty(find(ind==p+M+1))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end     
    ind_sub=[];
    %按照B6结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p-1)) && ~isempty(find(ind==p+M-1)) && ~isempty(find(ind==p+M)) &&...
                isempty(find(ind==p+1)) && isempty(find(ind==p-M+1)) && isempty(find(ind==p-M))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end    
    ind_sub=[];
    %按照B7结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p+M-1)) && ~isempty(find(ind==p+M)) && ~isempty(find(ind==p+M+1)) &&...
                isempty(find(ind==p-M-1)) && isempty(find(ind==p-M)) && isempty(find(ind==p-M+1))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end   
    ind_sub=[];
    %按照B8结构元素搜索
    for i=1:length(ind)
        p=ind(i,1);
        if ~isempty(find(ind==p+1)) && ~isempty(find(ind==p+M)) && ~isempty(find(ind==p+M+1)) &&...
                isempty(find(ind==p-1)) && isempty(find(ind==p-M)) && isempty(find(ind==p-M-1))
            ind_sub=cat(1,ind_sub,i);
        end
    end
    if ~isempty(ind_sub)
        ind(ind_sub)=[];
    end 
end            
%m连通检测
ind_c=[];
while ~isequal(ind_c,ind)
    ind_c=ind;    
    ind_back=ind;    
    while ~isempty(ind_back)
        p=ind_back(1,:);
        %如果p点四联通中有三个值为1，则将该点置为零
        if (~isempty(find(ind==p+1)) && ~isempty(find(ind==p+M)) && ~isempty(find(ind==p-M))) ||...
                (~isempty(find(ind==p-1)) && ~isempty(find(ind==p+M)) && ~isempty(find(ind==p-M))) ||...
                (~isempty(find(ind==p+1)) && ~isempty(find(ind==p-1)) && ~isempty(find(ind==p-M))) ||...
                (~isempty(find(ind==p+1)) && ~isempty(find(ind==p-1)) && ~isempty(find(ind==p+M)))
            c=find(ind==p);
            ind(c)=[];
 
        end
        %如果p点四联通中有两个值为1，且其对角为0，则将该点置为零
        if (~isempty(find(ind==p+1)) && ~isempty(find(ind==p+M)) && isempty(find(ind==p-M-1))) ||...
                (~isempty(find(ind==p-1)) && ~isempty(find(ind==p+M)) && isempty(find(ind==p-M+1))) ||...
                (~isempty(find(ind==p+1)) && ~isempty(find(ind==p-M)) && isempty(find(ind==p+M-1))) ||...
                (~isempty(find(ind==p-1)) && ~isempty(find(ind==p-M)) && isempty(find(ind==p+M+1)))
            c=find(ind==p);
            ind(c)=[];
        end             
        ind_back(1,:)=[];
    end       
end
 
%删除扩展的边缘
g=zeros(size(I_pad));
g(ind)=1;
g=g(2:M-1,2:N-1);
end