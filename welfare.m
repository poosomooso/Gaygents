% Matlab Code by JOSUE ORTEGA, University of Glasgow, used in the article
% "Social Integration via Online Dating: The Strength of Weak Ties"
% For more information: http://www.josueortega.com/research

% Three functions are defined. Welfare computes the diversity, strength, and size of
% a given society. Simul1 vectorizes it. Simul2 allows for MonteCarlo simulations.

function [race,avgdist,number]=welfare(n,m,p,q,type)
%Inputs 
%n:# of agents
%m:# of races
%p: prob on intraconnection
%q: prob of interconnection
%type: k-path marriages, 1 direct, 2 long
%Outputs
%number: SIZE
%avgdistance: AVERAGE DISTANCE
%race: DIVERSITY
%SECTION 1: EDGES
%Part 1.1: Creating genders                                                
%Cleans screen 
k=round((.5*n));                                  
%Minimum quota of women
temp = [ones(m,k), zeros(m,k), round(rand(m,n-2*k))]; 
%Creates required women, like this
%     1     1     0     0     1
%     1     1     0     0     1
%     1     1     0     0     0
[~, idx] = sort( rand(m,n), 2);
%Creates something like this:
%       3     5     1     2     4
%       1     3     5     4     2
%       5     4     2     1     3
sex = temp(sub2ind(size(temp), ndgrid(1:m,1:n), idx));
%     0     1     1     1     0
%     1     0     1     0     1
%     0     0     1     1     0
women=find(sex');
%find all ones, lists them as a column
men=find(~sex');
%same with zeros
%Part 1.2: Creating personality traits
x1=rand(1,n*m); y1=rand(1,n*m); sex1=reshape(sex',1,n*m);
%Everything as a one row vector 
%SECTION 2: EDGES 
%Part 2.1: Interracial edges
adj=zeros(m*n); 
%Adjacency matrix
boxes=(((m-1)*m)/2)*n^2;
%Number of race boxes in each adjacency matrix times number of people %in each box, i.e. number of interracial edges
inter_edges=randsample(boxes,floor(boxes*q));
rr=1;
for i=1:(m*n)
    for j=n+floor((i-1)/n)*n+1:(m*n)
        if i~=j
        if any(rr==inter_edges)
            adj(i,j)=1;
        end
        rr=rr+1;
        end
    end
end
%with m=2,n=3,q=1 looks like this
%     0     0     0     1     1     1
%     0     0     0     1     1     1
%     0     0     0     1     1     1
%     0     0     0     0     0     0
%     0     0     0     0     0     0
%     0     0     0     0     0     0
%Part 2.2: Intraracial edges
intra_edges=rand(n*m);rr=0;
for i=1:n*m
    rr=floor((i-1)/n);
    for j=i+1:(rr*n)+n
        if intra_edges(i,j)<p %
            adj(i,j)=1; 
        end
    end
end
%Self explanatory, really: creating inter links
adj=triu(adj,-1)+triu(adj)';
%Preserving symmetry of adjacency matrix
%WARNING: Part only needed for LONG marriages
adj2=adj*adj;
%adj2 tell us if there is a path connecting two persons of length 2
adj3=zeros(m*n);
for i=1:m*n
    for j=i+1:m*n
        if adj2(i,j)+adj(i,j)>0
        adj3(i,j)=1;
        end
    end
end
adj3=triu(adj3,-1)+triu(adj3)';
%adj3 tells us if there is a path OF AT MOST length 2
if type==1
    adj3=adj;
elseif type==2
    adj3=adj3;
else
    msg = 'Wrong input, 1 or 2 path only.';
    error(msg)
end
 
%SECTION 3: DISTANCES
distance=zeros(n*m,m*n);
for i=1:m*n
    for j=i:m*n
        if i==j
            distance(i,j)=NaN;
%You can?t marry yourself
        else
            if adj3(i,j)==0 %WARNING, KEY, switch to adj for direct
                distance(i,j)=NaN;
                %You can?t marry someone you don?t know
            else
                if sex1(i)==sex1(j)
                    distance(i,j)=NaN;
                    %Heterosexual marriage only
                else
                    distance(i,j)=sqrt((x1(i) - x1(j))^2 + (y1(i) - y1(j))^2);
                    %WARNING: Euclidean societies here! 
                end
            end
        end
    end
end
distance=triu(distance,-1)+triu(distance)';
%Keeping distance symmetric
%WARNING: This is not true for assortative societies
 
%SECTION 4: MARRIAGES
marr=zeros(1,m*n);
%marr: people pointing to their closest
marriage=zeros(1,m*n);
%marriage: final partner
for i=1:n*m
    [~, marr(1,i)]=min(distance(i,:));
end
%everybody points to their best
c=1;
while c <= 2*max(nnz(sex),numel(sex)-nnz(sex))
%nnz(sex): number of women
%numel(sex)-nnz(sex): number of men
%c<:because you can only point to how many women are available
for i=1:n*m
    if i==marr(marr(i));
        %mutual pointing
        marriage(i)=marr(i);
    end
end
for i=find(marriage==0)
    if marriage(marr(i))~=0;
    distance(i, marr(i))=NaN;
    %If someone is married, we block him for everybody else and they %  %have to point someone else
    end
end
for i=1:n*m
    [~, marr(1,i)]=min(distance(i,:));
end
c=c+1;
end
for i=1:m*n
    if marriage(i)==i
        marriage(i)=0;
    end
end
%SECTION 5: WELFARE MEASURES
number=size(find(marriage),2)/2;
%We need to divide because counts how many married people
avgdist=0;
for i=find(marriage>0)
    avgdist=avgdist+distance(i,marriage(i));
end
avgdist=avgdist/size(find(marriage>0),2);
race=0;
for i=1:m*n
    if marriage(i)>0
        if marriage(i)<=(1+floor((i-1)/n))*n && marriage(i)>floor((i-1)/n)*n
            race=race+1;
    end
    end
end
%race is now the number of intraracial marriages
race=race/2;race=number-race;race=(race/number)/((m-1)/m);
number=(number*2)/(m*n);
avgdist=(sqrt(2)-avgdist)/sqrt(2);
end

function [race,avgdist,number] = simul1(n,m,p,q,type)
[~, r]=size(q);
number=zeros(1,r);
avgdist=zeros(1,1);
race=zeros(1,r);
for i=1:r
[race(i),avgdist(i),number(i)]=welfare(n,m,p,q(i),type);
end
end

function [race,avgdist,number] = simul2(rep,n,m,p,q,type);
[~, sizeq]=size(q);
RACE=zeros(rep,sizeq);
AVGDIST=zeros(rep,sizeq);
NUMBER=zeros(rep,sizeq);
parfor i=1:rep
    [RACE(i,:), AVGDIST(i,:), NUMBER(i,:)]=simul1(n,m,p,q,type);
end
race=sum(RACE)/rep;
avgdist=sum(AVGDIST)/rep;
number=sum(NUMBER)/rep;
if type==1
    disp('direct marr')
else
    disp('long marr')
end
end