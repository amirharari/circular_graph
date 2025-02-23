load CM
CM(CM>100)=100;

%% assign segments
cm1=brewermap(85,'*Reds');
cm2=brewermap(70,'*Blues');
cm3=brewermap(48,'*Greens');
cm4=brewermap(32,'*Purples');
cm5=brewermap(28,'*Oranges');
cm6=brewermap(135,'*YlOrRd');
cm7=brewermap(35,'*Greys');
cmap=[cm1(1:68,:)', cm2(1:56,:)', cm3(1:38,:)', cm4(1:26,:)', cm5(1:22,:)', cm6(99:end,:)', cm7(1:28,:)']';
ocmap=cmap;



%% Show Circular Graph
figure
locs=[1:2:273 274:-2:1];
hold on
cmap=ocmap(locs,:);
save xcmap cmap;
% PL2=zeros(274,274);
% PL2(1:246,1:246)=PL.*30;
conmat2=CM(locs,locs);
conmat2(find(conmat2>0))=0;
conm=abs(conmat2);
conm(find(conm<280))=0;
conm(isnan(conm)) = 0;
circularGraph(conm);

%% the pie
hold on
nv=ones(1,274);
explode=nv;
labels=repmat({''}, 274, 1);
labels{7}='L Ce';
labels{274-7}='R Ce';
labels{23}='L SubCor';
labels{274-23}='R SubCor';
labels{38}='L Oc';
labels{274-38}='R Oc';
labels{50}='L Ins/Lim';
labels{274-50}='R Ins/Lim';
labels{66}='L Pa';
labels{274-66}='R Pa';
labels{89}='L Te';
labels{274-89}='R Te';
labels{120}='L Fr';
labels{274-120}='R Fr';
h=pie(nv,explode,labels);
set(h,'EdgeColor','none')
set(findobj(h,'type','text'),'fontsize',20);
cmap2=cmap([138:274, 1:137],:);
colormap((cmap2));
r=1; %radius
x0=0;y0=0; % circle center coordinates
x=x0-r:0.01:x0+r;
y=sqrt(r^2-(x-x0).^2)+y0;
h2=fill(x,y,'w',x,-y,'w');
set(h2,'EdgeColor','none')
axis equal
axis off

